/**
 * QQChat - Have a chat between CS:GO Server and QQ.
 *          Makesure [message channel] has been deployed!
 * by CarOL
 * visit https://docs.csgowiki.top/message-channel
 * 
 * Changelog:
 * 0.1   - 25.08.2021: Functional testing
 */

#pragma semicolon 1
#pragma newdecls required

#include <sourcemod>
#include <ripext>
#include <socket>

#define LENGTH_NAME 32
#define LENGTH_MESSAGE 128

Handle g_hSocket;

public Plugin myinfo = {
	name = "[CSGOWiki] QQChat",
	author = "CarOL",
	description = "Just Chat!",
	version = "v0.1",
	url = "https://docs.csgowiki.top/message-channel"
}

public void OnPluginStart() {
}

public void OnConfigsExecuted() {
    g_hSocket = SocketCreate(SOCKET_TCP, OnSocketError);
    SocketSetOption(g_hSocket, SocketReuseAddr, 1);
    SocketBind(g_hSocket, "0.0.0.0", 54321);
    SocketListen(g_hSocket, OnSocketIncoming);
}

public Action OnSocketIncoming(Handle socket, Handle newSocket, char[] remoteIP, int remotePort, any arg) {
    SocketSetReceiveCallback(newSocket, OnSocketReceive);
	SocketSetDisconnectCallback(newSocket, OnSocketDisconnected);
	SocketSetErrorCallback(newSocket, OnSocketError);
}

public Action OnSocketError(Handle socket, const int errorType, const int errorNum, any args) {
	// a socket error occured
	LogError("socket error %d (errno %d)", errorType, errorNum);
	CloseHandle(socket);
}

public Action OnSocketReceive(Handle socket, char[] receiveData, const int dataSize, any hFile) {
	// send (echo) the received data back
    PrintToServer("[QQChat] receive: %s", receiveData);
    if (dataSize <= 1 || receiveData[0] != '{') {
        PrintToServer("[Socket] receive error: %s", receiveData);
        return;
    }
    JSONObject json_obj = JSONObject.FromString(receiveData);
    char sender[LENGTH_NAME];
    char message[LENGTH_MESSAGE];
    int msg_type = json_obj.GetInt("message_type");
    json_obj.GetString("sender", sender, sizeof(sender));
    json_obj.GetString("message", message, sizeof(message));

    if (msg_type == 0) {
        PrintToChatAll("[\x09QQ\x01] \x04%s\x01：%s", sender, message);
        PrintToServer("[QQ] \x04%s\x01：%s", sender, message);
    }
    delete json_obj;
	SocketSend(socket, "ok", -1);
	// close the connection/socket/handle if it matches quit
	// if (strncmp(receiveData, "quit", 4) == 0) CloseHandle(socket);
}

public Action OnSocketDisconnected(Handle socket, any args) {
	// remote side disconnected
	CloseHandle(socket);
}
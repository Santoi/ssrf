<?php
// Define the host and port
$host = '10.0.0.5';
$port = 9090;

// Allow requests from any origin
header("Access-Control-Allow-Origin: *");
// Allow specified methods
header("Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS");
// Content type
header('Content-Type: application/json');
// Start the PHP built-in web server
echo "Starting PHP server at http://$host:$port\n";
echo "Press Ctrl+C to stop the server\n";

// Handle incoming requests

// Accept incoming connections
$socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
socket_bind($socket, $host, $port);
socket_listen($socket);
    
while (true) {
    // Accept incoming connections
    $client = socket_accept($socket);

    // Read data from the client
    $request = socket_read($client, 1024);
    echo "Received request: $request\n";

    // Include endpoint handler
    include 'requester.php';
    handleRequest($client, $request);
    
    // Close the client socket
    socket_close($client);
}


<?php
// Function to handle the GET endpoint
function handleRequest($client, $request) {
    // Parse the request
    $parsedRequest = parseRequest($request);

    // Check if it's a GET request and has an 'input' parameter
    if ($parsedRequest['method'] === 'GET' && isset($parsedRequest['query']['inputUrl'])) {
        // Extract the input parameter
        $input = $parsedRequest['query']['inputUrl'];

        // Send back a response with the received input
        $response = "HTTP/1.1 200 OK\nContent-Type: text/plain\n\nReceived input: $input";
        http_response_code(200);
        // Return the parsed URL as JSON
        echo json_encode($input);
    } else {
        http_response_code(404);
        // Send a 404 Not Found response for unsupported requests
        $response = "HTTP/1.1 404 Not Found\nContent-Type: text/plain\n\n404 Not Found";
    }

    // Send the response back to the client
    socket_write($client, $response);
    return;
}

// Function to parse the HTTP request and extract the method, path, and query parameters
function parseRequest($request) {
    $parsedRequest = array();

    // Split the request into lines
    $lines = explode("\n", $request);

    // Parse the first line to extract method, path, and protocol
    $firstLineParts = explode(" ", $lines[0]);
    $parsedRequest['method'] = $firstLineParts[0];
    $parsedRequest['path'] = $firstLineParts[1];
    $parsedRequest['protocol'] = $firstLineParts[2];
    echo "method: " . $parsedRequest['method'] . "\n";
    echo "path: " . $parsedRequest['path'] . "\n";
    echo "protocol: " . $parsedRequest['protocol'] . "\n";

    // Parse query parameters from the path
    $queryPos = strpos($parsedRequest['path'], '?');
    if ($queryPos !== false) {
        $queryString = substr($parsedRequest['path'], $queryPos + 1);
        parse_str($queryString, $parsedRequest['query']);
    } else {
        $parsedRequest['query'] = array();
    }

    echo "query: " . $parsedRequest['query']['inputUrl'] . "\n";
    return $parsedRequest;
}
?>


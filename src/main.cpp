#include <iostream>
#include <vector>
#include "httplib.h"
#include "json.h"
#include <unistd.h>

using json = nlohmann::json;

int main2(int agrc, char* argv[]) {
    const char* server_address = "http://ckprojects.herokuapp.com";

    // Create an HTTP client
    httplib::Client client(server_address);

    // Set up the request path and parameters (if any)
    std::string request_path = "/cpp-test"; // Replace with your endpoint path

    // Create a vector and convert it to a JSON string
    std::vector<std::vector<int>> data = {{1}, {2}, {3}, {4}, {5}};
    json json_data(data); // Updated this line

    std::string json_string = json_data.dump();

    // Set up the HTTP POST headers
    httplib::Headers headers = {
        {"Content-Type", "application/json"},
        {"Content-Length", std::to_string(json_string.length())}
    };
    sleep(15); // Pause for 15 seconds
    // Send an HTTP POST request with the JSON data
    auto response = client.Post(request_path.c_str(), headers, json_string, "application/json");

    // Check the response status and print the response body
    if (response && response->status == 200) {
        std::cout << "Response: " << response->body << std::endl;
    } else {
        std::cerr << "Failed to send HTTP request" << std::endl;
    }

    return 0;
}

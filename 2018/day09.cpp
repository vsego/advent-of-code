#include <algorithm>
#include <deque>
#include <fstream>
#include <iostream>
#include <list>
#include <regex>
#include <vector>

typedef std::vector<int> pair;

long long int solve(int num_players, int max_points) {
    std::deque<int> marbles = {0};
    long long int players[num_players] = {};

    for (int marble = 1; marble <= max_points; marble++) {
        if (marble % 23) {
            for (int k = 0; k < 2; k++) {
                marbles.push_back(marbles.front());
                marbles.pop_front();
            }
            marbles.push_front(marble);
        } else {
            for (int k = 0; k < 6; k++) {
                marbles.push_front(marbles.back());
                marbles.pop_back();
            }
            players[marble % num_players] += marbles.back() + marble;
            marbles.pop_back();
        }
        /*
        std::deque<int>::iterator it;
        std::cout << "[" << (marble % num_players) << "] ";
        for (it = marbles.begin(); it != marbles.end(); it++)
            std::cout << " " << *it;
        std::cout << std::endl;
        */
    }
    return *std::max_element(players, players + num_players);
}

int main() {
    std::list<pair> tests = {
        pair({9, 25}), pair({10, 1618}), pair({13, 7999}), pair({17, 1104}),
        pair({21, 6111}), pair({30, 5807}),
    };

    std::fstream fp("day09.in", std::ios_base::in);
    std::regex re_input("(\\d+) players; last marble is worth (\\d+) points");
    std::smatch re_res;
    std::string input;
    std::getline(fp, input);
    std::regex_search(input, re_res, re_input);
    int num_players(std::stoi(re_res[1].str()));
    int max_points(std::stoi(re_res[2].str()));

    std::list<pair>::iterator test_it;
    int which = 0;
    for (test_it = tests.begin(); test_it != tests.end(); test_it++) {
        std::cout << "Test " << ++which << ": ";
        std::cout << solve((*test_it)[0], (*test_it)[1]) << std::endl;
    }

    std::cout << "Part 1: " << solve(num_players, max_points) << std::endl;
    std::cout << "Part 2: " << solve(num_players, 100 * max_points) << std::endl;

    return 0;
}

#!/usr/bin/node

const request = require('request');

// Get the movie ID from the command line argument
const movieId = process.argv[2];

// Base URL for the Star Wars API
const apiUrl = `https://swapi.dev/api/films/${movieId}/`;

// Send a request to the SWAPI for the given movie
request(apiUrl, (error, response, body) => {
    if (!error && response.statusCode === 200) {
        const filmData = JSON.parse(body);
        
        // Get the list of character URLs from the film data
        const characters = filmData.characters;

        // Loop through each character URL and fetch the character name
        characters.forEach(characterUrl => {
            request(characterUrl, (error, response, body) => {
                if (!error && response.statusCode === 200) {
                    const characterData = JSON.parse(body);
                    console.log(characterData.name);
                }
            });
        });
    } else {
        console.error('Failed to retrieve the movie data.');
    }
});

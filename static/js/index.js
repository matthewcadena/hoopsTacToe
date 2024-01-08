const searchInput = document.getElementById('searchInput');
const searchResultsContainer = document.getElementById('search-results-container');
let activeSquare = null;

// starts a new game, called after 'new game' button is clicked after a game is won
function startNewGame() {
    window.location.href = '/game/';
}

// event listener for clicks in any of the squares
document.querySelectorAll('.button').forEach(button => {
    button.addEventListener('click', function () {
         fetch(`/button_click/${parseInt(this.id)}`)
        .then(response => response.json())
        .then(data => {
            // only make changes if the square has not been taken
            if (data.result === 'open') {
                const searchResults = document.getElementById('search-results-container');
                if (searchResults.classList.contains('hidden')) {
                    activeSquare = this.id;
                    toggleSearchBarVisibility();
                }
                const searchTerm = this.innerText.trim();
                performSearch(searchTerm);
            }
        });
    });
});

// checks to see if a player has won the game, called each time a correct answer is given
function checkGameOver() {
    fetch(`/check_game/`)
        .then(response => response.json())
        .then(data => {
            if (data.game_over === 'true') {
                // show game over screen if the game is won
                let message = '';
                if (data.winner === 'cat') message = "Cat's game";
                else message = `Player ${data.winner} Wins`;
                document.getElementById('winner-subtext').innerText = message;
                document.getElementById('game-over-screen').style.display = 'flex';
                document.getElementById('turn-indicator').style.display = 'none';
        }
    });
}

// checks if answers are valid, calls views.check_player
function checkAndSetSquare(square, player){
    fetch(`/check_player/?square=${square}&player=${player}`)
        .then(response => response.json())
        .then(data => {
            const activeSquare = document.getElementById(square);
            const turnIndicator = document.getElementById('turn-indicator');
            // set the square's color to red if it's player 1's guess and blue if it's player 2's
            if (data.result.valid === 'true') {
                activeSquare.innerText = player
                if (data.result.turn === '1') {
                    activeSquare.style.backgroundColor = '#17408B';
                } else {
                    activeSquare.style.backgroundColor = '#C9082A';
                }
            } else {
                (alert("incorrect!"));
                activeSquare.style.backgroundColor = "#36454f";
            }
            // set the color and text of the turn indicator to the next player
            if (data.result.turn === '1') {
                turnIndicator.style.backgroundColor = '#C9082A';
                turnIndicator.innerText = "Player 1's Turn";
            }
            else {
                turnIndicator.style.backgroundColor = '#17408B';
                turnIndicator.innerText = "Player 2's Turn";
            }
            checkGameOver();
        })
        .catch(error => {
        console.error('Error:', error);
    });
}

// event listener for search results so players can be chosen
document.getElementById('search-results-container').addEventListener('click',
                                                                       function (event) {
    if (event.target.tagName === 'LI') {
        const selectedPlayer = event.target.textContent;
        if (activeSquare != null) {
            checkAndSetSquare(activeSquare, selectedPlayer);}
        toggleSearchBarVisibility();
    }
});

// turns search bar on and off when buttons are clicked and players are chosen
function toggleSearchBarVisibility() {
    const searchContainer = document.querySelector('.search');
    const searchResults = document.getElementById('search-results-container')
    searchContainer.classList.toggle('hidden');
    searchResults.classList.toggle('hidden');
}

// event listener for when the input to the search bar changes
searchInput.addEventListener('input', function () {
    const searchTerm = this.value.trim();
    performSearch(searchTerm)
        .then(results => {
            if (results.length > 0 && results.length !== 2535) {  // don't display results if it includes all players
                displaySearchResults(results);
            } else {
                hideSearchResults();
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
});

// queries a local fine (players.json) and retrieves players that contain the search input
function performSearch(query) {
    const playersDataUrl = '/get_players_data/';
    return $.ajax({
        url: playersDataUrl,
        method: 'GET',
        dataType: 'json',
    })
        .then(playersData => {
            query = (query || '').toLowerCase();
            const filteredData = playersData.filter(player => {
                return ((player.player_name || '').toLowerCase()).includes(query);
        });
            return Promise.resolve(filteredData);
        })
          .fail(error => {
            console.error('Error fetching player data:', error);
            return Promise.reject(error);
        });
}

// displays relevant search results based on user input
function displaySearchResults(results) {
    searchResultsContainer.innerHTML = '';
    const resultList = document.createElement('ul');
    // only remove the rounded corners of the bottom of the search bar if there are results to display
    if (results.length > 0 ){
        document.querySelector('.search').style.borderBottomRightRadius = '0';
        document.querySelector('.search').style.borderBottomLeftRadius = '0';
    }
    resultList.style.listStyleType = 'none';
    results.forEach(result => {
        const listItem = document.createElement('li');
        listItem.textContent = result.player_name;
        resultList.appendChild(listItem);
    });
    searchResultsContainer.appendChild(resultList);
    searchResultsContainer.style.display = 'block';
}

function hideSearchResults() {
    // round the bottom corners of the search bar
    document.querySelector('.search').style.borderRadius = '28px';
    searchResultsContainer.style.display = 'none';
}

// clears previously selected buttons so that only the most recently selected is highlighted
function clearButtons() {
    const buttonIDs = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    for (let i = 0; i < buttonIDs.length; i++)  {
        let button = document.getElementById(buttonIDs[i]);
        if (button.style.backgroundColor === 'rgb(142, 142, 142)') {
            button.style.backgroundColor = '#36454f';
        }
    }
}

// highlights the button clicked by the user if it's available
function buttonClick(buttonNumber) {
    fetch(`/button_click/${buttonNumber}`)
        .then(response => response.json())
        .then(data => {
            activeSquare = buttonNumber;
            clearButtons();
            if (data.result === 'open') {
                document.getElementById(buttonNumber).style.backgroundColor = 'rgb(142, 142, 142)';
            }
        });
}
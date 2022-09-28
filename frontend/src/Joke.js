import React, {useEffect, useState} from "react";

function Joke() {
    const[joke, setJoke] = useState({});

    useEffect(() => {
        fetch('https://official-joke-api.appspot.com/jokes/random')
            .then(response => response.json())
            .then(json => {
                console.log('joke json', json);
                setJoke(json);
            });
        console.log('fetching data');
    }, []);

    const {setup, punchline} = joke;
    // const setup = joke.setup;
    // const punchline = joke.punchline;

    return(
        <div>
            <h3>Joke</h3>
            <p>{setup}</p>
            <p><em>{punchline}</em></p>
        </div>
    )
}

export default Joke;
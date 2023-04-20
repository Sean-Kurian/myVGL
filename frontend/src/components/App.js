import React, { Component } from "react";
import { render } from "react-dom";

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      data: [],
      loaded: false,
      placeholder: "Loading"
    };
  }

  componentDidMount() {
    fetch("api/game/")
      .then(response => {
        if (response.status > 400) {
          return this.setState(() => {
            return { placeholder: "Something went wrong!" };
          });
        }
        return response.json();
      })
      .then(data => {
        this.setState(() => {
          return {
            data,
            loaded: true
          };
        });
      });
  }

  render() {
    const { data, loaded, placeholder } = this.state;

    if (!loaded) {
      return <div>{placeholder}</div>;
    }

    return (
      <table>
        <thead>
          <tr>
            <th>Title</th>
            <th>Release Date</th>
            <th>Platforms</th>
            <th>Developers</th>
            <th>Publishers</th>
            <th>Genres</th>
          </tr>
        </thead>
        <tbody>
          {data.map(game => (
            <tr key={game.id}>
              <td>{game.title}</td>
              <td>{game.release_date}</td>
              <td>
                {game.platforms.map(platform => (
                  <div key={platform.id}>{platform.name}</div>
                ))}
              </td>
              <td>
                {game.developers.map(developer => (
                  <div key={developer.id}>{developer.name}</div>
                ))}
              </td>
              <td>
                {game.publishers.map(publisher => (
                  <div key={publisher.id}>{publisher.name}</div>
                ))}
              </td>
              <td>
                {game.genres.map(genre => (
                  <div key={genre.id}>{genre.name}</div>
                ))}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    );
  }
}

export default App;

const container = document.getElementById("app");
render(<App />, container);
import React from 'react';
import axios from 'axios';


class App extends React.Component {
	state ={
		venues: []
	}
  componentDidMount() {
    axios.get(`http://localhost:5000/venues`)
      .then(res => {
        const venues = res.data.data.children.map(obj => obj.data);
        this.setState({ venues });
        console.log(res)
      });
  }

	render(){
		return <div>PETS!PETS!PETS!</div>
	}
}

export default App
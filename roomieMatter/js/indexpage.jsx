import React from "react";
import PropTypes from "prop-types";

class StatusButton extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
        status: "Loading...",
        };
    }

    componentDidMount() {
        fetch(this.props.url)
        .then((res) => res.json())
        .then(
            (data) => {
            this.setState({
                status: data.status,
            });
            },
        );
    }

    handleClick() {
        fetch(this.props.url, {
            method: "POST",
        })
        .then((res) => res.json())
        .then(
            (data) => {
            this.setState({
                status: data.status,
            });
            },
        );
    }

    render() {
        return (
            <div className="margin_top_20">
                <span className="cuteFont_medium">You Are: </span>
            <button className="statusButton" onClick={() => this.handleClick()}>
                {this.state.status}
            </button>
            </div>
        );
    }
}

class RoomieList extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            roomies: [],
        };
        this.fetchData = this.fetchData.bind(this);
    }

    componentDidMount() {
        this.fetchData();
        setInterval(this.fetchData, 2000);
    }

    fetchData() {
        fetch(this.props.url)
        .then((res) => res.json())
        .then(
            (data) => {
                this.setState({
                    roomies: data['roomies'],
                });
            },
        );
    }
            
    render() {
        const { roomies } = this.state;
        if (roomies.length === 0) {
            return (<p className="roomie">Go get some roomies!</p>);
        }
        return (
            <ul className="center">
                {roomies.map((roomie) => (
                    <li key={roomie.name}>
                        <p className="roomie">
                        <span className="fontWeight1000">{roomie.name}</span> - {roomie.status}
                        </p>
                    </li>
                ))}
            </ul>
        );
    }
}

function IndexPage() {
    return (
        <div>
            <StatusButton url="/api/status" />
            <p className="main80 top30px">Your Roomies:</p>
            <RoomieList url="/api/roomies" />
        </div>
    );
}

export default IndexPage;


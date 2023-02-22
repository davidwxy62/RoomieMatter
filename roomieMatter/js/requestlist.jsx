import React from "react";
import PropTypes from "prop-types";
// import { useNavigate } from "react-router-dom";

class Redirect extends React.Component {
    constructor(props) {
        super(props);
    }

    componentDidMount() {
        window.location.href = this.props.to;
    }

    render() {
        return null;
    }
}


function Request({name, onAccept, onReject}) {
    return (
        <span>
            <span className="display-6 name">{name} - </span>
            <button className="cuteButton_small" onClick={onAccept}>Accept</button> &nbsp;
            <button className="cuteButton_small" onClick={onReject}>Reject</button>
        </span>
    );
}

class RequestList extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            mounted: false,
            requests: [],
        };
        this.handleAccept = this.handleAccept.bind(this);
        this.handleReject = this.handleReject.bind(this);
    }

    componentDidMount() {
        fetch(this.props.url)
        .then((res) => res.json())
        .then(
            (data) => {
            this.setState({
                mounted: true,
                requests: data.requests,
            });
            },
        );
    }

    handleAccept(senderId) {
        fetch(this.props.url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                senderId: senderId,
            }),
        })
        .then((res) => {if (res.ok) {
            this.setState((prevState) => ({
                requests: prevState.requests.filter((request) => request.senderId !== senderId),
            }));
        }});
    }

    handleReject(senderId) {
        fetch(this.props.url, {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                senderId: senderId,
            }),
        })
        .then((res) => {if (res.ok) {
            this.setState((prevState) => ({
                requests: prevState.requests.filter((request) => request.senderId !== senderId),
            }));
        }});
    }

    render() {
        const { mounted, requests } = this.state;
        if (mounted && requests.length === 0) {
            return (
                <Redirect to='/'/>
            );
        }
        return (
                requests.map((request) => (
                    <li key={requests.senderId}>
                        <Request 
                        name={request.name}
                        onAccept={() => this.handleAccept(request.senderId)}
                        onReject={() => this.handleReject(request.senderId)}
                        />
                    </li>
                ))
        );
    }
}

RequestList.propTypes = {
    url: PropTypes.string.isRequired,
};
export default RequestList;
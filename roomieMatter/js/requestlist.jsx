import React from "react";
import PropTypes from "prop-types";

function Request({name, onAccept, onReject}) {
    return (
        <span>
            <span className="roomie">{name} - </span>
            <button className="cuteButton_small" onClick={onAccept}>Accept</button>
            <span className="roomie"> </span>
            <button className="cuteButton_small" onClick={onReject}>Reject</button>
        </span>
    );
}

class RequestList extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            requests: [],
        };
        this.handleAccept = this.handleAccept.bind(this);
        this.handleReject = this.handleReject.bind(this);
    }

    componentDidMount() {
        fetch(this.props.url)
        .then((res) => res.json())
        .then(
            (result) => {
            this.setState({
                requests: result.requests,
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
        return (
            <div className="margin_top_20">
                <span className="main50">Pending Requests: </span>
                <ul>
                    {this.state.requests.map((request) => (
                        <li key={request.senderId}>
                            <Request 
                            name={request.name}
                            onAccept={() => this.handleAccept(request.senderId)}
                            onReject={() => this.handleReject(request.senderId)}
                            />
                        </li>
                    ))}
                </ul>
            </div>
        );
    }
}

RequestList.propTypes = {
    url: PropTypes.string.isRequired,
    };
export default RequestList;
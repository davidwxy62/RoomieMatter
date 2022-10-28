import React from "react";
import PropTypes from "prop-types";
// import { useNavigate } from "react-router-dom";

// class Redirect extends React.Component {
//     constructor(props) {
//         super(props);
//     }

//     componentDidMount() {
//         window.location.href = this.props.to;
//     }

//     render() {
//         return null;
//     }
// }


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
            (data) => {
            this.setState({
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
            if (this.state.requests.length === 0) {
                window.location.href = "/";
            }
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
            if (this.state.requests.length === 0) {
                window.location.href = "/";
            }
        }});
    }

    render() {
        const { requests } = this.state;
        // if (requests.length === 0) {
        //     return (
        //         <Redirect to='/'/>
        //     );
        // }
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
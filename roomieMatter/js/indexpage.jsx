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
            mounted: false,
        };
        this.fetchData = this.fetchData.bind(this);
        this.notifContent = this.notifContent.bind(this);
    }

    componentDidMount() {
        if (typeof Notification !== "undefined" && Notification.permission !== "granted") {
            Notification.requestPermission();
        }
        this.fetchData();
        setInterval(this.fetchData, 10000); // Make it slower later so server doesn't get overloaded
    }

    fetchData() {
        if (document.hasFocus()) {
            fetch(this.props.url)
            .then((res) => res.json())
            .then(
                (data) => {
                    this.setState({
                        roomies: data.roomies,
                        mounted: true,
                    });
                    console.log("mounted")
                    const { roomies } = this.state;
                    let notif = this.notifContent(data.roomies, roomies);              
                    if (Object.keys(notif).length > 0) { // There are notifications
                        if (typeof Notification !== "undefined" && Notification.permission === "granted") {
                            if ('new_roomie' in notif) {
                                new Notification("New Roomie!", {
                                    body: 'Welcome ' + notif['new_roomie'].join(', '),
                                });
                            } else {
                                let body_str = '';
                                for (let [key, value] of Object.entries(notif)) {
                                    body_str += key + ' is now ' + value + '.\n';
                                }
                                new Notification("Status Change!", {
                                    body: body_str,
                                });
                            }
                        } 
                    }
                }
            );
        }
    }
            
    notifContent(new_arr, old_arr) {
        let notif = {}

        // Return nothing if someone left the room
        if (new_arr.length < old_arr.length || old_arr.length === 0) {
            return notif;
        }

        let new_names = new_arr.map((roomie) => roomie.name);
        let old_names = old_arr.map((roomie) => roomie.name);
        let new_status = new_arr.map((roomie) => roomie.status);
        let old_status = old_arr.map((roomie) => roomie.status);

        // Check if there are any new roomies
        if (new_names.length > old_names.length) {
            for (let i = 0; i < new_names.length; i++) {
                if (old_names.indexOf(new_names[i]) === -1) {
                    if (!('new_roomie' in notif)) {
                        notif['new_roomie'] = [];
                    }
                    notif['new_roomie'].push(new_names[i]);
                } 
            }
            return notif;
        }

        // Check if there are any status changes
        for (let i = 0; i < new_names.length; i++) {
            if (new_status[i] !== old_status[i]) {
                notif[new_names[i]] = new_status[i];
            }
        }
        return notif;
    }

    render() {
        const { roomies, mounted } = this.state;
        if (roomies.length === 0 && mounted ) {
            return (<p className="roomie">Go get some roomies!</p>);
        }
        return (
                roomies.map((roomie) => (
                        <li key={roomie.name} className="center roomie fontWeight1000">
                            <span>{roomie.name} - {roomie.status}</span>
                        </li>
                ))
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


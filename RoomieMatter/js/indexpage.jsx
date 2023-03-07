import React from "react";

class StatusButton extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            status: "Loading...",
            name: "Loading...",
        };
    }

    componentDidMount() {
        fetch(this.props.url)
        .then((res) => res.json())
        .then(
            (data) => {
                this.setState({
                    status: data.status,
                    name: data.name,
                });
            },
        );
        setInterval(() => this.fetchData(), 5000);
    }

    fetchData() {
        fetch("api/status")
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
    // timeout
    

    render() {
        const { status, name } = this.state;
        return (
            <div>
                <span className="display-6 name">{name} - </span>
                <button className="cuteButton" onClick={() => this.handleClick()}>
                    <span className="rem-2_5">{status}</span>
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
        setInterval(() => this.fetchData(), 5000);
    }

    fetchData() {
            fetch(this.props.url)
            .then((res) => res.json())
            .then(
                (data) => {
                    this.setState({
                        roomies: data.roomies,
                        mounted: true,
                    });
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
        const { roomies, mounted, last_refresh } = this.state;
        if (roomies.length === 0 && mounted ) {
            return (<p className="name mt-5 display-6">Go get some roomies!</p>);
        }
        return (
            <div className="mt-5 ">
                {roomies.map((roomie) => (
                    <ul>
                        <li key={roomie.name}>
                            <span className="display-6 name">{roomie.name}</span>
                            <span className="display-6 status"> - {roomie.status}</span>
                        </li>
                    </ul>
                ))}
            </div>
        );
    }
}

function IndexPage() {
    return (
        <div>
            <div className="row mx-auto">
                <div className="col-6 mx-auto">
                    <StatusButton url="/api/status" />
                </div>
            </div>
            <div className="row mx-auto">
                <div className="col-6 mx-auto">
                    <RoomieList url="/api/roomies" />
                </div>
            </div>
        </div>
    );
}

export default IndexPage;


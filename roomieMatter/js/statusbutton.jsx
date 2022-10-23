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
            (result) => {
            this.setState({
                status: result.status,
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
            (result) => {
            this.setState({
                status: result.status,
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

StatusButton.propTypes = {
    url: PropTypes.string.isRequired,
  };
  export default StatusButton;
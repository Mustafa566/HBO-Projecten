import React, { Component } from "react";
import { Col, Container, Row } from "reactstrap";
import UserList from "../components/user_list/userlist";
import axios from "axios";
import { API_URL_USERS }from "../constants";

class Users extends Component {
    state = {
        users: []
    };

    componentDidMount() {
        this.resetState();
    }
    
    getUsers = () => {
        axios.get(API_URL_USERS).then(
            res => this.setState({
                users: res.data
            })
        );
    };

    resetState = () => {
        this.getUsers();
    };

    render() {
        return (
            <Container style={{ marginTop: "20px" }}>
                <Row>
                    <Col>
                        <UserList
                            users={this.state.users}
                            resetState={this.resetState}
                        />
                    </Col>
                </Row>
            </Container>
        )
    }
}

export default Users
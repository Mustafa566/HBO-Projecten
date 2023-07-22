import React, { Component } from "react";
import { Col, Container, Row } from "reactstrap";
import McQuestionList from "../components/mcQuestions/McQuestionList";
import NewMcQuestionModal from "../components/mcQuestions/NewMcQuestionModal";
import axios from "axios";
import { API_URL_MC_Q } from "../constants";


class McQuestions extends Component {
    state = {
        mcQuestions: [],
    };

    componentDidMount() {
        this.resetState();
    }

    getMcQuestions = () => {
        axios.get(API_URL_MC_Q).then(
            res => this.setState({
                mcQuestions: res.data
            })
        );
    };

    // Refreshes the table and displays questions and mc options
    resetState = () => {
        this.getMcQuestions();
    };

    handleNewMcQuestion = () => {
        this.resetState();
    };

    render() {
        return (
            <Container style={{ marginTop: "20px" }}>
                <Row
                    className="justify-content-center"
                >
                    <Col
                        className="col-md-9"
                    >
                        <McQuestionList
                            mcQuestions={this.state.mcQuestions}
                            resetState={this.resetState}
                        />
                    </Col>
                </Row>
                <Row>
                    <Col
                        className="col-md-5 text-center"
                    >
                        <NewMcQuestionModal
                            create={true}
                            resetState={this.resetState}
                            getMcQuestions={this.getMcQuestions}
                            onQuestionCreated={this.handleNewMcQuestion}
                            />
                    </Col>
                </Row>
            </Container>
        )
    }
}

export default McQuestions;
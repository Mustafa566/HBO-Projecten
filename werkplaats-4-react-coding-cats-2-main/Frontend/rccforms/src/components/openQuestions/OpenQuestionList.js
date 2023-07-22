import React, { Component, Fragment } from "react";
import { Table, Button } from "reactstrap";
import axios from "axios";
import {
    API_URL_OPEN_Q,
    API_URL_HIDE_OPEN_Q,
} from "../../constants";
import NewOpenQuestionModal from "./NewOpenQuestionModal";


class OpenQuestionList extends Component {
    // Default state of the component with an empty list of questions,
    // Empty list of multiple choice options,
    // refreshing of the list is false (only activated when Verbergen button is clicked)
    state = {
        questions: [],
        refresh: false
    };

    // Preparations before the component appears on screen (mounts).
    // In this case: retrieve open questions from the database
    // before the OpenQuestionList appears on screen.
    componentDidMount() {
        this.getOpenQuestions();
    }

    // Retrieves all open questions from database that are not set as hidden
    getOpenQuestions = () => {
        axios
            .get(API_URL_OPEN_Q)
            .then((res) => {
                const filteredOpenQ = res.data.filter(
                    (openQ) => !openQ.is_hidden
                );
                this.setState({
                    questions: filteredOpenQ.map((openQ) => ({
                        ...openQ,
                        is_hidden: false,
                    })),
                });
            })
    };

    // When you click on the Verbergen button, the is_hidden boolean
    // changes to True and the question also gets hidden from the table
    // because the only questions where is_hidden = false are allowed to be listed.
    handleHideOpenQuestion = (openQuestionId) => {
        axios
            .put(`${API_URL_HIDE_OPEN_Q}${openQuestionId}/hide/`)
            .then((response) => {
                if (response.data.success) {
                    this.setState((prevState) => ({
                        questions: prevState.questions.filter(
                            (openQ) => openQ.question_id !== openQuestionId
                        ),
                    }));
                    this.refreshOpenQuestionList();
                } else {
                    console.log(response.data.error);
                }
            })
            .catch((error) => {
                console.log(error);
            });
    };

    // Refreshes the OpenQuestionList component so the change is
    // immediately visible: hidden questions are filtered out.
    refreshOpenQuestionList = () => {
        this.getOpenQuestions();
        this.refreshPage();
    };

    render() {
        // Constant for open question state defined above: empty question list
        const openQuestions = this.state.questions;

        // Constants for the refresh state variable
        const { refresh } = this.state;

        // Constant for the visible open questions: questions where is_hidden is false
        const visibleOpenQuestions = openQuestions.filter(openQ => !openQ.is_hidden);

        // If refresh occurs, get the open questions from database and
        // set the state of refresh to false again.
        if (refresh) {
            this.getOpenQuestions();
            this.setState({ refresh: false });
        }

        // Structure and content of what should be rendered on the screen
        return (
            <Fragment>
            <Table
                hover
                striped
            >
                <thead>
                <tr>
                    <th>#</th>
                    <th>Vraag</th>
                    {/* Edit button column */}
                    <th></th>
                    {/* Hide question button column */}
                    <th></th>
                </tr>
                </thead>
                <tbody>
                {/* Condition: if there are no open questions where is_hidden = false in the database
                then the sentence in <b> tags will be displayed. */}
                {!visibleOpenQuestions || visibleOpenQuestions.length <= 0 ? (
                    <tr>
                        <td colSpan="6" align="center">
                            <b>Nog geen vragen in de database.</b>
                        </td>
                    </tr>
                //    Else if visibleOpenQuestions is not empty, map over each element in the array,
                //    render a table row for each question.
                ) : (
                    visibleOpenQuestions.map((openQ) => {
                        if (!visibleOpenQuestions.includes(openQ)) {
                            return null;
                        }

                        return (
                            // Return the columns from the questions database
                            <tr key={openQ.pk}>
                                <th scope="row">{openQ.question_id}</th>
                                <td>{openQ.question_text}</td>
                                <td align="center">
                                    {/* Display the modal to edit questions when Wijzigen button is clicked */}
                                    <NewOpenQuestionModal
                                        create={false}
                                        question={openQ}
                                        resetState={this.props.resetState}
                                        getOpenQuestions={this.getOpenQuestions}
                                        refreshOpenQuestionList={this.refreshOpenQuestionList}
                                    />
                                </td>
                                <td align="center">
                                        {/* Display the button that hides questions */}
                                        <Button
                                            color="danger"
                                            size="sm"
                                            onClick={() => this.handleHideOpenQuestion(openQ.question_id)}
                                        >
                                            Verbergen
                                        </Button>
                                    </td>
                            </tr>
                            );
                    })
                )}
                </tbody>
            </Table>
            </Fragment>
        );
    }
}

export default OpenQuestionList;
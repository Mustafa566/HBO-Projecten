import React, { Component, Fragment } from "react";
import { Table, Button } from "reactstrap";
import axios from "axios";
import {
    API_URL_MC_Q,
    API_URL_HIDE_MC_Q
} from "../../constants";
import NewMcQuestionModal from "./NewMcQuestionModal";


class McQuestionList extends Component {
    // Default state of the component with an empty list of questions,
    // Empty list of multiple choice options,
    // refreshing of the list is false (only activated when Verbergen button is clicked)
    state = {
        questions: [],
        refresh: false
    };

    // Preparations before the component appears on screen (mounts).
    // In this case: retrieve mc questions from the database
    // before the McQuestionList appears on screen.
    componentDidMount() {
        this.getMcQuestions();
    }

    // Retrieves all mc questions from database that are not set as hidden
    getMcQuestions = () => {
        axios
            .get(API_URL_MC_Q)
            .then((res) => {
                const filteredMcQ = res.data.filter(
                    (mcQ) => !mcQ.is_hidden
                );
                this.setState({
                    questions: filteredMcQ.map((mcQ) => ({
                        ...mcQ,
                        is_hidden: false,
                    })),
                });
            })
    };

    // When you click on the Verbergen button, the is_hidden boolean
    // changes to True and the question also gets hidden from the table
    // because the only questions where is_hidden = false are allowed to be listed.
    handleHideMcQuestion = (mcQuestionId) => {
        axios
            .put(`${API_URL_HIDE_MC_Q}${mcQuestionId}/hide/`)
            .then((response) => {
                if (response.data.success) {
                    this.setState((prevState) => ({
                        questions: prevState.questions.filter(
                            (mcQ) => mcQ.mc_id !== mcQuestionId
                        ),
                    }));
                    this.refreshMcQuestionList();
                } else {
                    console.log(response.data.error);
                }
            })
            .catch((error) => {
                console.log(error);
            });
    };

    // Refreshes the McQuestionList component so the change is
    // immediately visible: hidden questions are filtered out.
    refreshMcQuestionList = () => {
        this.getMcQuestions();
        this.refreshPage();
    };

    render() {
        // Constant for mc question state defined above: empty question list
        const mcQuestions = this.state.questions;

        // Constants for the refresh state variable
        const { refresh } = this.state;

        // Constant for the visible mc questions: questions where is_hidden is false
        const visibleMcQuestions = mcQuestions.filter(mcQ => !mcQ.is_hidden);

        // If refresh occurs, get the mc questions from database and
        // set the state of refresh to false again.
        if (refresh) {
            // this.getOpenQuestions();
            this.getMcQuestions();
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
                    <th>A</th>
                    <th>B</th>
                    <th>C</th>
                    <th>D</th>
                    {/* Edit button column */}
                    <th></th>
                    {/* Hide question button column */}
                    <th></th>
                </tr>
                </thead>
                <tbody>
                {/* Condition: if there are no mc questions where is_hidden = false in the database
                then the sentence in <b> tags will be displayed. */}
                {!visibleMcQuestions || visibleMcQuestions.length <= 0 ? (
                    <tr>
                        <td colSpan="6" align="center">
                            <b>Nog geen vragen in de database.</b>
                        </td>
                    </tr>
                //    Else if visibleMcQuestions is not empty, map over each element in the array,
                //    render a table row for each question.
                ) : (
                    visibleMcQuestions.map((mcQ) => {
                        if (!visibleMcQuestions.includes(mcQ)) {
                            return null;
                        }

                        return (
                            // Return the columns from the questions database
                            <tr key={mcQ.pk}>
                                <th>{mcQ.mc_id}</th>
                                <td>{mcQ.question_text}</td>
                                <td>{mcQ.option_a}</td>
                                <td>{mcQ.option_b}</td>
                                <td>{mcQ.option_c}</td>
                                <td>{mcQ.option_d}</td>
                                <td align="center">
                                    {/* Display the modal to edit questions when Wijzigen button is clicked */}
                                    <NewMcQuestionModal
                                        create={false}
                                        question={mcQ}
                                        resetState={this.props.resetState}
                                        getMcQuestions={this.getMcQuestions}
                                        refreshMcQuestionList={this.refreshMcQuestionList}
                                    />
                                </td>
                                <td align="center">
                                        {/* Display the button that hides questions */}
                                        <Button
                                            color="danger"
                                            size="sm"
                                            onClick={() => this.handleHideMcQuestion(mcQ.mc_id)}
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

export default McQuestionList;
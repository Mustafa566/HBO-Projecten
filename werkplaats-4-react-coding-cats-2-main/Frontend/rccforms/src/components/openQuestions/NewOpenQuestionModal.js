// Code inspired by
// https://blog.logrocket.com/using-react-django-create-app-tutorial/

import React, { Component, Fragment } from "react";
import { Button, Modal, ModalHeader, ModalBody } from "reactstrap";
import NewOpenQuestionForm from "./NewOpenQuestionForm";


class NewOpenQuestionModal extends Component {
    // Default state of the modal where the modal is not active
    state = {
        modal: false,
    };

    // Handles the activation of the modal
    toggle = () => {
        this.setState(previous => ({
            modal: !previous.modal
        }));
    };

    refreshPage = () => {
        window.location.reload();
    }

    render() {
        // Assigns the value of the prop 'create' to the constant 'create'
        // Same for the modal
        const create = this.props.create;
        const modal = this.state.modal;

        // Title of the modal when 'Wijzigen' button is clicked
        let title = "Vraag aanpassen";
        // 'Wijzigen' button displayed in the table rows that activates the modal
        let button =
            <Button onClick={this.toggle} size="sm">
                Wijzigen
            </Button>;

        // When create is activated, the title should be different and
        // the button that activates the modal will also be different
        if (create) {
            title = "Nieuwe vraag toevoegen";
            button = (
                <Button
                    color="primary"
                    onClick={this.toggle}
                    style={{ minWidth: "200px", margin: "0 auto"}}
                    >
                    Toevoegen
                </Button>
            );
        }

        return (
            <Fragment>
                {/* Button variable for Toevoegen or Wijzigen */}
                {button}
                {/* Modal (or i.e. this component) is open when button (toggle) is clicked */}
                <Modal
                    isOpen={modal}
                    toggle={this.toggle}
                    >
                    {/* Modal header is visible when modal is open and
                    shows a title based on which button is clicked to activate it */}
                    <ModalHeader
                        toggle={this.toggle}>
                        {title}
                    </ModalHeader>

                    {/* Renders the form to add a new question in the body of the modal. */}
                    <ModalBody>
                        <NewOpenQuestionForm
                            create={this.props.create}
                            resetState={this.props.resetState}
                            toggle={this.toggle}
                            getOpenQuestions={this.props.getOpenQuestions}
                            onQuestionCreated={this.props.onQuestionCreated}
                            question={this.props.question}
                            />
                    </ModalBody>
                </Modal>
            </Fragment>
        )
    }
}

export default NewOpenQuestionModal;
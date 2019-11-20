import React, { Component } from 'react'

class Cim extends Component {
    constructor(props) {
        super(props)
        this.state = {
            branch: 'cim',
            className: '',
            instanceName: '',
            method: '',
                      result: ''}
        

        this.handlechange = this.handlechange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);

    }
        handlechange(event) {
            const target = event.target;
            const value = target.value;
            const name = target.name;
            this.setState({
                [name] : value
            });
}
       
        handleSubmit(event) {
            event.preventDefault();

            fetch("http://localhost:8000", {
                method: "post",
                headers: {
                    'Accept': 'application/json',
                    'Content-Type' : 'application/json'
                },

                body: JSON.stringify(this.state)
                })
                .then( (response) => response.text())
                    .then((body) => {
                        this.setState({
                            result: body.replace(/(?:\r\n|\r|\n)/g, '<br>')
                        })
                    })
                
        }
    

    render() {
        return (
        <div>
            <div className="container-fluid ">
        <form onSubmit={this.handleSubmit}>
            <div className="row">
            <label>
                CIM operation:  
                <select value={this.state.method} name = 'method' onChange={this.handlechange}>
                    <option value="enumerateInstances">Enumerate instances </option>
                    <option value="enumerateInstanceNames">Enumerate instance names</option>
                    <option value="getInstance">Get instance</option>
                    <option value="enumerateClassNames">Enumerate classnames</option>
                    <option value="enumerateClasses">Enumerate classes</option>
                    <option value="getClass">Get class</option>
                </select>
            </label>
            </div>
            <div className="row">
            <label>
                Class Name:
                <input type="text" value = {this.state.className} onChange=
                {this.handlechange} name='className' />
            </label>
            </div>
            <div className="row">
            <label>
                Instance Name:
                <input type="text" value = {this.state.instanceName} onChange=
                {this.handlechange} name='instanceName' />
            </label>
            </div>

            <div className="row">
            <input type="submit" value="Submit" />
            </div>
            </form>
            <div className="row">
                <div dangerouslySetInnerHTML={{__html: this.state.result}} />
            </div>
            </div>
        </div>
        );
    }
}

export default Cim
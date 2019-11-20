import React, { Component } from 'react'

class Snmp extends Component {
    constructor(props) {
        super(props)
        this.state = {
                        branch: 'snmp',
                        method: 'smpget',
                      result: '',
                      oid: ''}
        

        this.handlechange = this.handlechange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);

    }
        handlechange(event) {
            console.log("change is working");
            const target = event.target;
            const value = target.value;
            const name = target.name;
            this.setState({
                [name] : value
            });
}
       
        handleSubmit(event) {
            console.log("submit is working)");
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
                    <option value="snmpget">get request </option>
                    <option value="snmpgetnext">get-next request</option>
                    <option value="snmpbulkget">bulk request</option>
                    <option value="snmpwalk">snmp walk</option>
                    <option value="snmptable">Snmp Table</option>
                </select>
            </label>
            </div>
            <div className="row">
            <label>
                OID:
                <input type="text" value = {this.state.oid} onChange=
                {this.handlechange} name='oid' />
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

export default Snmp
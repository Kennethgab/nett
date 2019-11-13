import React, { Component } from 'react';
import Cim from './components/Cim.jsx'
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Link,
    Redirect
} from "react-router-dom";


class Shell extends Component {
    constructor(props) {
        super(props)

        this.state = {
                 
        }
    }

    render() {
        return (
            <Router>
                <div>
                    <nav>
                        <ul>
                            <li>
                                <Link to="/CIM">CIM</Link>
                            </li>
                            <li>
                                <Link to="/SNMP">SNMP</Link>
                            </li>
                        </ul>
                    </nav>
                </div>

                <Switch>
                    <Route path="/CIM">
                        <Cim />
                    </Route>
                    <Route path="/SNMP">
                        <Cim />
                        </Route>
                    <Redirect from="/" to="/cim" />
                </Switch>
            </Router>
       )
    }
}

export default Shell

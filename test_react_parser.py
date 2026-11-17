from tree_sitter import Language, Parser
import tree_sitter_javascript as tsjavascript
from backend.app.parsers.javascript_parser import JavaScriptParser

language = Language(tsjavascript.language())
parser = Parser(language)

code = """
import React, { useState, useEffect } from 'react';

function UserCard({ name, age }) {
    const [active, setActive] = useState(false);

    useEffect(() => {
        console.log(name);
    }, [name]);

    return (
        <div className="card">
            <h2>{name}</h2>
            <p>{age}</p>
            <button onClick={() => setActive(!active)}>
                Toggle
            </button>
        </div>
    );
}

const App = () => {
    return <UserCard name="Harsh" age={21} />;
};
"""

parser = JavaScriptParser()
result = parser.parse(code)

print(result)
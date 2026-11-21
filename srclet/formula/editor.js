"use strict";
MathfieldElement.fontsDirectory = "./fonts";
MathfieldElement.soundsDirectory = null;
const field = document.getElementById("field");
field.mathVirtualKeyboardPolicy = "manual";
field.smartFence = true;
field.menuItems = [];
let initialLatex, initialExpression;
function openFormula(latex, expression) {
    field.value = latex || (expression === null ? "" : LatexSyntax.serialize(expression));
    initialLatex=field.value;
    initialExpression=expression;
    field.focus();
}
function insertMath(template) {
    field.focus();
    field.executeCommand(["insert", template, {selectionMode: "placeholder"}]);
}
function readFormula() {
    try {
        return JSON.stringify({latex: field.value, expression: field.value === initialLatex && initialExpression != null ? initialExpression : LatexSyntax.parse(field.value)});
    } catch (error) {
        return JSON.stringify({error: String(error)});
    }
}

function selectUnknownSymbol(symbol) {
    // MathLive uses atom offsets for selections, including nested fractions.
    for (let start = 0; start < field.lastOffset; start++) {
        const limit = Math.min(field.lastOffset, start + symbol.length + 3);
        for (let end = start + 1; end <= limit; end++) {
            const text = field.getValue(start, end, "latex")
                .replace(/\\(?:mathrm|mathit|operatorname)\b/g, "")
                .replace(/[{}\\\s]/g, "");
            if (text === symbol) {
                field.focus();
                field.selection = { ranges: [[start, end]] };
                return;
            }
        }
    }
}

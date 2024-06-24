(function () {
    const calculator = function (hook, vm) {
        let objects = {};
        let results = []; // [{"formula": "x", "result": "y"}]
        let db = {};

        function runCode(code) {
            try {
                const run = new Function(
                    ...Object.keys(objects),
                    'updateList',
                    'db',
                    code
                );
                return run(
                    ...Object.values(objects),
                    updateList,
                    db
                );
            } catch (error) {
                console.log("Error running code: " + code);
                console.log("Log: " + error);
                return "";
            }
        }

        function updateCalculations() {
            for (let i = 0; i < results.length; i++) {
                try {
                    const calculation = new Function(
                        ...Object.keys(objects),
                        'db',
                        `return ${results[i]["formula"]}`
                    );
                    results[i]["result"].value = calculation(...Object.values(objects), db);
                } catch (error) {
                    results[i]["result"].value = 'Error in calculation';
                }
            }
        }

        function updateList(list, content) {
            // Remove all old list options
            const options = list.getElementsByTagName('option');
            while (options.length > 0) {
                options[0].parentNode.removeChild(options[0]);
            }

            // Create new list objects
            content.forEach(obj => {
                option = document.createElement('option');
                if (typeof obj === 'string') {
                    option.textContent = obj;
                    option.value = obj;
                } else {
                    option.value = obj["value"] || obj["name"];
                    option.textContent = obj["name"];
                }
                list.appendChild(option);
            })
            list.selectedIndex = 0;
            list.dispatchEvent(new Event('input', { bubbles: true }));
        }

        function addSetup({ code }) {
            objects["calcStartupFunction"] = code;
        }

        function addFunction({ name, code, args = [] }) {
            const func = new Function(
                ...args,
                `with (this) { ${code} }`
            );
            objects[name] = func.bind(objects);
        }

        function createInput(
            {
                varName,
                label = null,
                type = null,
                value = null,
                placeholder = null,
                onChange = null,
                prefix = null,
                suffix = null,
                help = null,
                readOnly = false,
                disabled = false
            },
            margin = "mb-3"
        ) {
            const div = document.createElement('div');
            div.className = margin;

            if (label) {
                const labelText = document.createElement('label');
                labelText.htmlFor = 'floatingInput';
                labelText.innerText = label;
                div.appendChild(labelText);
            }

            const group = document.createElement("div");
            group.className = "input-group";

            if (prefix) {
                const prefixText = document.createElement("span");
                prefixText.className = "input-group-text";
                prefixText.textContent = prefix;
                group.appendChild(prefixText);
            }

            const input = document.createElement('input');
            objects[varName] = input;
            input.className = 'form-control';
            input.id = "floatingInput";
            if (placeholder) {
                input.placeholder = placeholder;
            }
            if (type) {
                input.type = type;
            }
            if (value) {
                input.value = value;
            }
            input.readOnly = readOnly;
            input.disabled = disabled;

            input.addEventListener('input', (e) => {
                if (onChange) {
                    runCode(onChange);
                }
                updateCalculations();
            });
            group.appendChild(input);

            if (suffix) {
                const suffixText = document.createElement("span");
                suffixText.className = "input-group-text";
                suffixText.textContent = suffix;
                group.appendChild(suffixText);
            }

            div.appendChild(group);

            if (help) {
                const helpText = document.createElement("div");
                helpText.className = "form-text";
                helpText.innerText = help;
                div.appendChild(helpText);
            }

            return div
        }

        function createList(
            {
                varName,
                label = null,
                placeholder = null,
                list = null,
                generate = null,
                onChange = null,
                prefix = null,
                suffix = null,
                help = null,
                readOnly = false,
                disabled = false
            },
            margin = "mb-3"
        ) {
            const div = document.createElement('div');
            div.className = margin;

            if (label) {
                const labelText = document.createElement('label');
                labelText.htmlFor = 'floatingInput';
                if (label == " ") {
                    label = "\u00A0";
                }
                labelText.innerText = label;
                div.appendChild(labelText);
            }

            const group = document.createElement("div");
            group.className = "input-group";

            if (prefix) {
                const prefixText = document.createElement("span");
                prefixText.className = "input-group-text";
                prefixText.textContent = prefix;
                group.appendChild(prefixText);
            }

            const select = document.createElement('select');
            objects[varName] = select;
            select.className = 'form-select';
            select.id = "floatingSelect";
            select.readOnly = readOnly;
            select.disabled = disabled;
            if (placeholder) {
                const selected = document.createElement('option');
                selected.textContent = placeholder;
                selected.selected = true;
                select.appendChild(selected);
            }
            if (generate && typeof generate === 'string' && generate.length !== undefined) {
                list = runCode(generate);
            }
            if (list) {
                updateList(select, list);
            }

            select.addEventListener('input', (e) => {
                if (onChange) {
                    runCode(onChange);
                }
                updateCalculations();
            });
            group.appendChild(select);

            if (suffix) {
                const suffixText = document.createElement("span");
                suffixText.className = "input-group-text";
                suffixText.textContent = suffix;
                group.appendChild(suffixText);
            }

            div.appendChild(group);

            if (help) {
                const helpText = document.createElement("div");
                helpText.className = "form-text";
                helpText.innerText = help;
                div.appendChild(helpText);
            }

            return div
        }

        function createRules() {
            hr = document.createElement('hr');
            hr.className = "my-3 border-light-subtle";
            return hr
        }

        function createMulti(
            {
                label = null,
                content = null,
                help = null
            },
            margin = "mb-3"
        ) {
            const div = document.createElement('div');
            div.className = margin;

            if (label) {
                const labelText = document.createElement('label');
                labelText.htmlFor = 'floatingInput';
                labelText.innerText = label;
                div.appendChild(labelText);
            }

            const multi = document.createElement("div");
            multi.className = "input-group";

            content.forEach(obj => {
                createElement = elementFunctions[obj["element"]];
                if (createElement) {
                    element = createElement(obj, "");
                    while (element.children[0].childNodes.length > 0) {
                        multi.appendChild(element.children[0].childNodes[0]);
                    }
                }
            })

            div.appendChild(multi);

            if (help) {
                const helpText = document.createElement("div");
                helpText.className = "form-text";
                helpText.innerText = help;
                div.appendChild(helpText);
            }

            return div
        }

        function createGroup(
            {
                label = null,
                content = null,
                help = null,
                columns = 4,
                border = false
            },
            margin = "mb-3"
        ) {
            const div = document.createElement('div');
            div.className = margin;
            if (border == true) {
                div.className += ' border rounded p-3';
            }

            if (label) {
                const labelText = document.createElement('label');
                labelText.htmlFor = 'floatingInput';
                labelText.innerText = label;
                div.appendChild(labelText);
            }

            const group = document.createElement("div");
            const xl = "row-cols-xl-" + Math.max(columns, 1);
            const lg = "row-cols-lg-" + Math.max(columns - 1, 1);
            const sm = "row-cols-sm-" + Math.max(columns - 2, 1);
            const def = "row-cols-" + Math.max(columns - 3, 1);
            group.className = ["row g-3", def, sm, lg, xl].join(" ");
            content.forEach(obj => {
                createElement = elementFunctions[obj["element"]];
                if (createElement) {
                    element = createElement(obj, "");
                    col = document.createElement("div");
                    col.className = "col";
                    col.appendChild(element);
                    group.appendChild(col);
                }
            })

            div.appendChild(group);

            if (help) {
                const helpText = document.createElement("div");
                helpText.className = "form-text";
                helpText.innerText = help;
                div.appendChild(helpText);
            }

            return div
        }

        function createSum(
            {
                label = null,
                formula = null,
                prefix = null,
                suffix = null,
                help = null,
                disabled = false
            },
            margin = "mb-3"
        ) {
            const div = document.createElement('div');
            div.className = margin;

            if (label) {
                const labelText = document.createElement('label');
                labelText.htmlFor = 'floatingSum';
                labelText.innerText = label;
                div.appendChild(labelText);
            }

            const group = document.createElement("div");
            group.className = "input-group";

            if (prefix) {
                const prefixText = document.createElement("span");
                prefixText.className = "input-group-text";
                prefixText.textContent = prefix;
                group.appendChild(prefixText);
            }

            const input = document.createElement('input');
            input.className = 'form-control';
            input.id = "floatingSum";
            input.readOnly = true;
            input.disabled = disabled;
            group.appendChild(input);

            if (suffix) {
                const suffixText = document.createElement("span");
                suffixText.className = "input-group-text";
                suffixText.textContent = suffix;
                group.appendChild(suffixText);
            }

            div.appendChild(group);

            if (help) {
                const helpText = document.createElement("div");
                helpText.className = "form-text";
                helpText.innerText = help;
                div.appendChild(helpText);
            }

            results.push({
                "formula": formula.replace("\n", ""),
                "result": input,
            })
            return div
        }

        const elementFunctions = {
            setup: addSetup,
            function: addFunction,
            input: createInput,
            list: createList,
            rules: createRules,
            multi: createMulti,
            group: createGroup,
            sum: createSum
        };

        // Invoked one time when the docsify instance has mounted on the DOM
        hook.mounted(function () {
            // Access calculatorDB URL from Docsify configuration
            var calculatorDBUrl = $docsify["calculatorDB"];

            // Use the calculatorDB URL (e.g., fetch data from the URL)
            if (calculatorDBUrl) {
                fetch(calculatorDBUrl)
                    .then(response => response.json())
                    .then(data => {
                        db = data;
                    })
                    .catch(error => {
                        console.error("Error fetching calculatorDB:", error);
                    });
            }

            var calculatorTheme = $docsify["calculatorTheme"];
            if (calculatorTheme == "dark") {
                document.documentElement.setAttribute("data-bs-theme", "dark");
            }
        });

        // Invoked on each page load before new markdown is transformed to HTML
        hook.beforeEach(function (content) {
            Object.assign(objects, {});
            results = [];

            return content.replace(/```calculator([\s\S]*?)```/g, function (match, code) {
                return `<div class="calculator mt-2" hidden>${code.replace(/^\s+/gm, "").trim()}</div>`;
            });
        });

        // Invoked on each page load after new HTML has been appended to the DOM
        hook.doneEach(function () {
            const calculators = document.querySelectorAll('.calculator');
            calculators.forEach(calculator => {

                const data = JSON.parse("[" + calculator.innerText.replace(/[\n\r\t]/g, "") + "]");
                const elements = [];
                data.forEach(obj => {
                    const createElement = elementFunctions[obj["element"]];
                    if (createElement) {
                        objReturn = createElement(obj);
                        if (objReturn != null) {
                            elements.push(objReturn);
                        }
                    }
                });
                calculator.innerHTML = '';

                elements.forEach(el => calculator.appendChild(el));
                calculator.hidden = false;
            });

            // Run startup function if any
            runCode(objects["calcStartupFunction"]);
        });
    }

    // Add plugin to docsify's plugin array
    $docsify = $docsify || {};
    $docsify.plugins = [].concat(calculator, $docsify.plugins || []);
})();

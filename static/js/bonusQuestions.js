// you receive an array of objects which you must sort in the by the key "sortField" in the "sortDirection"
function getSortedItems(items, sortField, sortDirection) {
    if (sortDirection == "asc") {
        function compare(a, b) {
            if (a.Description < b.Description) {
                return -1;
            }
            if (a.Description > b.Description) {
                return 1;
            }
            return 0;
        }

        return items.sort(compare)
    } else {
        function compare(a, b) {
            if (a.Description > b.Description) {
                return -1;
            }
            if (a.Description < b.Description) {
                return 1;
            }
            return 0;
        }

        return items.sort(compare)
    }
}

// you receive an array of objects which you must filter by all it's keys to have a value matching "filterValue"
function getFilteredItems(items, filterValue) {

    let list = [];

    for (let i = 0; i < items.length; i++) {
        for (const [key, value] of Object.entries(items[i])) {
            if (key == "Title" || key == "Description") {
                if (filterValue.charAt(0) == "!") {
                    if (value.includes(filterValue.substring(1))) {
                        break;
                    } else if (filterValue.substring(1, 13) == "Description:") {
                        if (key == "Description") {
                            if (value.includes(filterValue.substring(13))) {
                                continue;
                            } else {
                                list.push(items[i])
                                break;
                            }
                        }
                    } else {
                        list.push(items[i])
                        break;
                    }
                } else if (filterValue.substring(0, 12) == "Description:") {
                    if (key == "Description") {
                        if (value.includes(filterValue.substring(12))) {
                            list.push(items[i])
                            break;
                        } else {
                            continue;
                        }
                    }

                } else {
                    if (value.includes(filterValue)) {
                        list.push(items[i]);
                        break;
                    } else {
                        continue;
                    }
                }
            }
        }
    }

    return list
}

function toggleTheme() {
    let x = document.getElementsByTagName("BODY")[0];
    x.style.backgroundColor = "black";
    x.style.color = "white";
}

function increaseFont() {
    let x = document.getElementsByTagName("table")[0];
    style = window.getComputedStyle(x, null).getPropertyValue('font-size');
    currentSize = parseFloat(style)
    if (currentSize < 25) {
        x.style.fontSize = (currentSize + 1) + 'px';
    }
}
function decreaseFont() {
    let x = document.getElementsByTagName("table")[0];
    style = window.getComputedStyle(x, null).getPropertyValue('font-size');
    currentSize = parseFloat(style)
    if (currentSize > 10) {
        x.style.fontSize = (currentSize - 1) + 'px';
    }
}
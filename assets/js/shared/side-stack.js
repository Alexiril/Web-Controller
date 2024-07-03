function makeStack(stackId, sides, max_size = -1) {
    let stack = $(`#${stackId}`);
    if (stack.length != 0)
        stack.remove();
    stack = $(`<div class="side-stack ${sides}" id="${stackId}" data-maxsize="${max_size}"></div>`);
    $("body").append(stack);
    return stack;
}

function addToStack(stackId, element) {
    let stack = $(`#${stackId}`);
    if (stack.length == 0)
        stack = makeStack(stackId, 'left-side bottom-side');
    const max_size = parseInt(stack.attr('data-maxsize'), 10);
    if (max_size != -1 && stack.children().length >= max_size)
        stack.children(":first").remove();
    element.hide();
    stack.append(element);
    element.fadeIn(200);
}

function clearStack(stackId) {
    let stack = $(`#${stackId}`);
    if (stack.length == 0)
        stack = makeStack(stackId, 'left-side bottom-side');
    stack.clear();
}
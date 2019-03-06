

function fadeSlideItems(element: any, i: number = null) {
    let len = element.children.length;
    if(i === null) {
        Array.from(element.children).forEach((el: HTMLElement) => { el.classList.add('hide') });
        i = 0;
    } else {
        element.children[i].classList.add('hide');
    }
    i++;
    element.children[i % len].classList.remove('hide');
    element.children[i % len].classList.add('elementToFadeInAndOut');
    setTimeout(() => fadeSlideItems(element, i % len), 8000);
}


document.addEventListener("DOMContentLoaded", function() {
    let elements: any = document.getElementsByClassName('fade-slide');
    Array.from(elements).forEach((el) => { fadeSlideItems(el) });
});

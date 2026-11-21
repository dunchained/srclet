const preview = document.querySelector("dialog");
for (const button of document.querySelectorAll("figure button")) {
    button.addEventListener("click", () => {
        const image = button.querySelector("img");
        preview.querySelector("img").src = image.src;
        preview.querySelector("img").alt = image.alt;
        preview.showModal();
    });
}
preview.querySelector("button").addEventListener("click", () => preview.close());
function openChapters(ids) {
    for (const chapter of document.querySelectorAll("details")) chapter.open = ids.includes(chapter.id);
}

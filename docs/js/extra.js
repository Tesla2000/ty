function cleanupClipboardText(targetSelector) {
  const targetElement = document.querySelector(targetSelector);

  // exclude "Generic Prompt" and "Generic Output" spans from copy
  const excludedClasses = ["gp", "go"];

  const clipboardText = Array.from(targetElement.childNodes)
    .filter(
      (node) =>
        !excludedClasses.some((className) =>
          node?.classList?.contains(className)
        )
    )
    .map((node) => node.textContent)
    .filter((s) => s != "");
  return clipboardText.join("").trim();
}

// Sets copy text to attributes lazily using an Intersection Observer.
function setCopyText() {
  // The `data-clipboard-text` attribute allows for customized content in the copy
  // See: https://www.npmjs.com/package/clipboard#copy-text-from-attribute
  const attr = "clipboardText";
  // all "copy" buttons whose target selector is a <code> element
  const elements = document.querySelectorAll(
    'button[data-clipboard-target$="code"]'
  );
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      // target in the viewport that have not been patched
      if (
        entry.intersectionRatio > 0 &&
        entry.target.dataset[attr] === undefined
      ) {
        entry.target.dataset[attr] = cleanupClipboardText(
          entry.target.dataset.clipboardTarget
        );
      }
    });
  });

  elements.forEach((elt) => {
    observer.observe(elt);
  });
}

// Using the document$ observable is particularly important if you are using instant loading since
// it will not result in a page refresh in the browser
// See `How to integrate with third-party JavaScript libraries` guideline:
// https://squidfunk.github.io/mkdocs-material/customization/?h=javascript#additional-javascript
document$.subscribe(function () {
  setCopyText();
});

// Use client-side redirects for anchors that have moved.
// Other redirects should use `redirect_maps` in the `mkdocs.yml` file instead.
(function () {
  // (there are no redirects yet)
  let redirect_maps = {};

  // The prefix for the site, see `site_dir` in `mkdocs.yml`
  let site_dir = "ty";

  function get_path() {
    var path = window.location.pathname;

    // Trim the site prefix
    if (path.startsWith("/" + site_dir + "/")) {
      path = path.slice(site_dir.length + 2);
    }

    // Always include a trailing `/`
    if (!path.endsWith("/")) {
      path = path + "/";
    }

    // Check for an anchor
    var anchor = window.location.hash.substring(1);
    if (!anchor) {
      return path;
    }

    return path + "#" + anchor;
  }

  let path = get_path();
  if (path && redirect_maps.hasOwnProperty(path)) {
    window.location.replace("/" + site_dir + "/" + redirect_maps[path]);
  }
})();

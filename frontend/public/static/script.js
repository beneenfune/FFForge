document.addEventListener("DOMContentLoaded", function () {
    var stage = new NGL.Stage("viewport");
    stage.loadFile("rcsb://1crn", {defaultRepresentation: true}).then(function (component) {
          // add a "cartoon" representation to the structure component
          component.addRepresentation("cartoon");
          // provide a "good" view of the structure
          component.autoView();
        });
});
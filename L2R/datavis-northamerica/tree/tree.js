// https://observablehq.com/@katy-li/collapsible-tree@373
export default function define(runtime, observer) {
  const main = runtime.module();
  //   main.variable(observer()).define(["md"], function (md) {
  //     return (
  //       md`# Collapsible Tree
  // This is a test of a data set we are trying to help staff understand, I forked from an existing collapsable tree and have been working through the code to slowly make edits and better understand how it was created.

  // Click a black node to expand or collapse [the tree](/@mbostock/d3-tidy-tree).`
  //     )
  //   });
  main.variable(observer("chart")).define("chart", ["d3", "data", "dy", "margin", "width", "dx", "tree", "diagonal"], function (d3, data, dy, margin, width, dx, tree, diagonal) {
    const root = d3.hierarchy(data);

    root.x0 = dy / 2;
    root.y0 = 0;
    root.descendants().forEach((d, i) => {
      d.id = i;
      d._children = d.children;
      if (d.depth && d.data.name.length !== 15) d.children = null;
    });

    const svg = d3.create("svg")
      .attr("viewBox", [-margin.left, -margin.top, width, dx])
      .style("font", "10px sans-serif")
      .style("user-select", "none");

    // add Linear Gradient 
    var svgDefs = svg.append('defs');
    var circleParent = svgDefs.append('linearGradient')
      .attr('id', 'circleParent');

    circleParent.append('stop')
      .attr('class', 'parent-left')
      .attr('offset', '0');

    circleParent.append('stop')
      .attr('class', 'parent-right')
      .attr('offset', '1');

    var circleChild = svgDefs.append('linearGradient')
      .attr('id', 'circleChild');

    circleChild.append('stop')
      .attr('class', 'child-left')
      .attr('offset', '0');

    circleChild.append('stop')
      .attr('class', 'child-right')
      .attr('offset', '1');

    // Add Path Files
    const gLink = svg.append("g")
      .attr("class", "lineGroup");
    // .attr("fill", "none")
    // .attr("stroke", "blue")
    // .attr("stroke-opacity", 0.8)
    // .attr("stroke-width", 1);

    const gNode = svg.append("g")
      .attr("cursor", "pointer")
      .attr("pointer-events", "all");

    const title = svg.append("text")
      .attr("class", "title language")
      .text("North America Language Family Tree");

    const footer = svg.append("text")
      .attr("class", "footer")
      .attr("text-anchor", "end")
      .text("Data source www.glottolog.org 2021");

    const credits = svg.append("text")
      .attr("class", "footer")
      .attr("text-anchor", "end")
      .text("Project of unfoldingword.org, designed & developed by ZetaLight");

    const legend = svg.append("g")
      .attr("class", "legend");

    const lroot = legend.append("g")
    lroot.append("rect")
      .attr("class", "fillRoot")
      .attr("rx", 4)
      .attr("ry", 4)
      .attr("width", 20)
      .attr("height", 20);
    lroot.append("text")
      .attr("y", 14)
      .attr("x", 26)
      .attr("class", "text")
      .text("Country");

    const lfamily = legend.append("g").attr("transform", d => "translate(0, 25)")
    lfamily.append("g")
      .append("rect")
      .attr("class", "fillFamily")
      .attr("rx", 4)
      .attr("ry", 4)
      .attr("width", 20)
      .attr("height", 20)
    lfamily.append("text")
      .attr("y", 14)
      .attr("x", 26)
      .attr("class", "text")
      .text("Family");

    const lparent = legend.append("g").attr("transform", d => "translate(0, 50)")
    lparent.append("g")
      .append("rect")
      .attr("class", "fillParent")
      .attr("rx", 4)
      .attr("ry", 4)
      .attr("width", 20)
      .attr("height", 20)
    lparent.append("text")
      .attr("y", 14)
      .attr("x", 26)
      .attr("class", "text")
      .text("Parent");

    const llanguage = legend.append("g").attr("transform", d => "translate(0, 75)")
    llanguage.append("g")
      .append("rect")
      .attr("class", "fillLanguage")
      .attr("rx", 4)
      .attr("ry", 4)
      .attr("width", 20)
      .attr("height", 20)
    llanguage.append("text")
      .attr("y", 14)
      .attr("x", 26)
      .attr("class", "text")
      .text("Language");

    const btn = svg.append("g")
      .attr("class", "button");

    const expandBtn = btn.append("g")
      .attr("id", "expand")
      .on("click", d => {
        expandAll()
      });

    const collapseBtn = btn.append("g")
      .attr("id", "collapse")
      .attr("transform", d => "translate(110, 0)")
      .on("click", d => {
        collapseAll()
      });

    expandBtn
      .append("rect")
      .attr("class", "expand")
      .attr("rx", 8)
      .attr("ry", 8)
      .attr("width", 90)
      .attr("height", 30);

    expandBtn
      .append("text")
      .attr("dy", "1.5em")
      .attr("x", 10)
      .attr("y", 1)
      .attr("class", "text btnText")
      // .attr("text-anchor", "start")
      .text("Expand All");

    collapseBtn
      .append("rect")
      .attr("class", "collapse")
      .attr("rx", 8)
      .attr("ry", 8)
      .attr("width", 100)
      .attr("height", 30);

    collapseBtn
      .append("text")
      .attr("dy", "1.5em")
      .attr("x", 10)
      .attr("y", 1)
      .attr("class", "text btnText")
      // .attr("text-anchor", "start")
      .text("Collapse All");

    function expand(d) {
      var children = (d.children) ? d.children : d._children;
      if (d._children) {
        d.children = d._children;
        d._children = null;
      }
      if (children)
        children.forEach(expand);
    }

    function expandAll() {
      console.log("expandAll");
      expand(root);
      update(root);
    }

    function collapse(d) {
      if (d.children) {
        d._children = d.children;
        d._children.forEach(collapse);
        d.children = null;
      }
    }

    function collapseAll() {
      console.log("collapseAll");
      root.children.forEach(collapse);
      // collapse(root);
      update(root);
    }



    function update(source) {
      const duration = d3.event && d3.event.altKey ? 2500 : 250;
      const nodes = root.descendants().reverse();
      const links = root.links();

      // Compute the new tree layout.
      tree(root);

      let left = root;
      let right = root;
      root.eachBefore(node => {
        if (node.x < left.x) left = node;
        if (node.x > right.x) right = node;
      });

      const height = right.x - left.x + margin.top + margin.bottom;

      // var bBox = svg.node().getBBox();
      // console.log('XxY : ', bBox.x + 'x : ' + bBox.y);
      // console.log('size : ', bBox.width + 'x : ' + bBox.height);

      const btns = svg.selectAll(".button")
      btns.attr("transform", d => `translate(${-margin.left + 120}, ${left.x - 15})`)
      console.log(height, margin.top, right.x);

      title.attr("transform", d => `translate(${width / 2 - 240}, ${left.x - 25})`)
      footer.attr("transform", d => `translate(${width - 60}, ${-(left.x - 20)})`)
      credits.attr("transform", d => `translate(${width - 60}, ${-(left.x - 40)})`)
      legend.attr("transform", d => `translate(${width - 240}, ${left.x - 25})`)


      const transition = svg.transition()
        .duration(duration)
        .attr("viewBox", [-margin.left, left.x - (margin.top + 20), width, height + 30])
        .tween("resize", window.ResizeObserver ? null : () => () => svg.dispatch("toggle"));


      // Update the nodes…
      const node = gNode.selectAll("g")
        .data(nodes, d => d.id);

      // Enter any new nodes at the parent's previous position.
      const nodeEnter = node.enter().append("g")
        .attr("transform", d => `translate(${source.y0},${source.x0})`)
        .attr("class", "box")
        // .attr("fill-opacity", 0)
        // .attr("stroke-opacity", 0)
        .on("click", d => {
          d.children = d.children ? null : d._children;
          update(d);
        });

      // nodeEnter.append("circle")
      //   .attr("r", 5)
      //   // .attr("x", 100)
      //   .attr("cx", "100%")
      //   // .attr("width", 10)
      //   // .attr("height", 10)
      //   .attr("fill", "none")
      //   // .attr("fill", d => d._children ? "#111" : "#333")
      //   // .attr("class", d => d._children ? "fillParent" : "fillChild")
      //   .attr("stroke-width", 1)
      //   .attr("stroke", "#000");



      nodeEnter.append("rect")
        .attr("class", function (d, i) {
          // console.log(d.depth);
          switch (d.depth) {
            case 1:
              return "fillFamily"
            case 2:
              return "fillParent"
            case 3:
              return "fillLanguage"
            default:
              return "fillRoot"
              break;
          }
        })
        .attr("x", 0)
        .attr("y", -12)
        .attr("rx", 8)
        .attr("ry", 8)
        .attr("width", function (d) {
          // console.log(d);
          let wordLength = d.data.name.length * 9.5;
          return wordLength;
        })
        .attr("height", 24)
      // .attr("fill", "#FFF")
      // .attr("stroke-width", 2)
      // .attr("stroke", "#000");
      // .attr("fill", "black");

      nodeEnter.append("text")
        .attr("dy", "1.5em")
        .attr("x", 9)
        // .attr("x", d => d._children ? 10 : 10)
        // .attr("y", d => d._children ? -10 : -10)
        .attr("y", -13.5)
        .attr("text-anchor", d => d._children ? "start" : "start")
        .attr("class",
          function (d, i) {
            // console.log(d.depth);
            switch (d.depth) {
              case 1:
                return "text family"
              case 2:
                return "text parent"
              case 3:
                return "text language"
              default:
                return "text root"
                break;
            }
          })
        .text(d => d.data.name);

      // .clone(true).lower()
      // .attr("stroke-linejoin", "round")
      // .attr("stroke-width", 3)
      // .attr("stroke", "white");



      // Transition nodes to their new position.
      const nodeUpdate = node.merge(nodeEnter).transition(transition)
        .attr("transform", d => `translate(${d.y},${d.x})`)
        .attr("fill-opacity", 1)
        .attr("stroke-opacity", 1);

      // Transition exiting nodes to the parent's new position.
      const nodeExit = node.exit().transition(transition).remove()
        .attr("transform", d => `translate(${source.y},${source.x})`)
        .attr("fill-opacity", 0)
        .attr("stroke-opacity", 0);

      // Update the links…
      const link = gLink.selectAll("path")
        .data(links, d => d.target.id);

      // Enter any new links at the parent's previous position.
      const linkEnter = link.enter().append("path")
        .attr("d", d => {
          const o = { x: source.x0, y: source.y0 };
          return diagonal({ source: o, target: o });
        });

      // Transition links to their new position.
      link.merge(linkEnter).transition(transition)
        .attr("d", diagonal);

      // Transition exiting nodes to the parent's new position.
      link.exit().transition(transition).remove()
        .attr("d", d => {
          const o = { x: source.x, y: source.y };
          return diagonal({ source: o, target: o });
        });

      // Stash the old positions for transition.
      root.eachBefore(d => {
        d.x0 = d.x;
        d.y0 = d.y;
      });

      // let groups = nodeEnter.selectAll('rect')._parents;
      // console.log(groups);
      // console.log(groups[0].children[1]);
      // console.log(groups[0].children[1].getBBox());
      // console.log(groups[0].getBBox());
      // console.log(groups[0].children[1].getBoundingClientRect()); //offsetWidth
      // console.log(groups[0].offsetWidth); //offsetWidth

      // nodeEnter.selectAll('text').attr("width", function (d) {
      //   console.log(d);
      // });

      // nodeEnter.selectAll('rect').attr("width", function (d) {
      //   // console.log(d);
      //   let wordLength = d.data.name.length * 9.5;
      //   return wordLength;
      // });
    }

    update(root);

    return svg.node();
  }
  );

  main.variable().define("diagonal", ["d3"], function (d3) {
    return (
      d3.linkHorizontal().x(d => d.y).y(d => d.x)
    )
  });
  main.variable().define("tree", ["d3", "dx", "dy"], function (d3, dx, dy) {
    return (
      d3.tree().nodeSize([dx, dy])
    )
  });
  main.variable().define("data", ["d3"], function (d3) {
    return (
      d3.json("/data/flare.json")
    )
  });
  main.variable().define("dx", function () {
    return (
      40
    )
  });
  main.variable().define("dy", ["width"], function (width) {
    return (
      width / 4
    )
  });
  main.variable().define("margin", function () {
    return (
      { top: 50, right: 50, bottom: 50, left: 50 }
    )
  });
  main.variable().define("d3", ["require"], function (require) {
    return (
      require("d3@5")
    )
  });
  return main;
}

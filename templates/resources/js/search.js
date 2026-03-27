document.addEventListener("DOMContentLoaded", function () {
  const input = document.getElementById("mkdocs-search-query");
  const sparqlResults = document.getElementById("mkdocs-search-results");

  input.addEventListener("input", function () {
    const query = input.value.trim();

    if (query.length < 2) {
      sparqlResults.innerHTML = "";
      return;
    }

    doSparqlSearch(query);
  });

function doSparqlSearch(query) {
  const endpoint = "http://localhost:8080/";

  const sparqlQuery = `
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?iri ?title WHERE {
      ?iri rdfs:label ?title .
      FILTER(CONTAINS(LCASE(?title), LCASE("${query}")))
    }
    LIMIT 10
  `;

  const url = endpoint + "?query=" + encodeURIComponent(sparqlQuery);

  fetch(url, {
    headers: {
      "Accept": "application/sparql-results+json"
    }
  })
    .then(res => res.json())
    .then(data => {
      renderSparqlResults(data.results.bindings);
    })
    .catch(err => {
      console.error(err);
    });
}

  function iriToPage(iri) {
  if (iri.startsWith(base_iri)) {
    return iri.replace(base_iri, base_url);
  }
  return iri; // fallback: external link
}


  function renderSparqlResults(results) {
    if (!results.length) {
      sparqlResults.innerHTML = "<p>No results</p>";
      return;
    }

  let html = "<ul>";

  results.forEach(r => {
    html += `
      <li>
        <h3>
          <a href="${iriToPage(r.iri.value)}">
            ${r.title.value}
          </a>
        </h3>
      </li>
    `;
  });

    html += "</ul>";
    sparqlResults.innerHTML = html;
  }
});
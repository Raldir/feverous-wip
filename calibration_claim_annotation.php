<?php
session_start();
// Start the session
// Check user login or not
if(!isset($_SESSION["user"]) ||  $_SESSION['annotation_mode'] != 'claim'){
    include file_get_contents('index.php');
    echo "<!--";
}
?>

<html>
<head>
  <link rel="stylesheet" href="css/style.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.1/css/bootstrap.min.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-select/1.13.1/css/bootstrap-select.css" />


  <script src="js/extensions/jquery.js"></script>
  <script src="js/extensions/jquery.md5.js"></script>
  <script src="js/extensions/jquery_scroll.js"></script>
  <script src="js/extensions/jquery_ui.js"></script>
  <script src="https://unpkg.com/@popperjs/core@2"></script>
  <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.1/js/bootstrap.bundle.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-select/1.13.1/js/bootstrap-select.min.js"></script>


  <script src="js/editable-select.js"></script>
  <script src="js/highlighter.js"></script>
  <script src="js/claim_annotation.js"></script>
</head>

<body style="font-family: sans-serif">

  <div class="topnav" id="myTopnav">
    <a href="user-details.php" id="user-details" class="fa fa-user-circle-o">User Details</a>
    <a href="annotation_guidelines/Claim_annotation/main.pdf" target="_blank" class="guidelines fa fa-file-pdf-o">Annotation Guidelines</a>
    <a href="" class="logout fa fa-sign-out" style="text-align:right">Logout</a>
    <a class="fa fa-exclamation" style="color:red; text-align:left"> CALIBRATION MODE. COMPLETE THE FOLLOWING ANNOATIONS AND RECEIVE FEEDBACK ON THEM. <i class='fa fa-exclamation'> </i></a>
  </div>

<div class="menu-frame" id="my-menu-frame">
  <div class="claim-generation-specifications">
    <!-- <label style="font-size:15px" for="claim_url">Title:</label> -->
    <p id='claim_url' style="font-size:15px"> No url retrieved. </p>
    <!-- <br>
    <label style="font-size:10px" for="selected_id">ID:</label>
    <p id='selected_id' style="font-size:10px"> No id retrieved. </p>
    <br>
    <br> -->
    <button id= 'go-back' class="btn btn-primary fa fa-arrow-circle-left fa-lg pull-left"></button>
    <button id= 'go-forward' class=" btn btn-primary fa fa-lg fa-arrow-circle-right pull-left" disabled></button>
  </div>

    <div class="generated-claim-div" id="generated-claim-div">
      <button type="button" class="btn btn-sm btn-info small h-5 fa fa-info rounded-circle" data-toggle="popover" data-html="true"  data-content="The first claim should exclusively use information from the highlighted table/sentences (including table captions/page title). The claim can either align with the contents in the highlight or contradict it. (i.e. true and false claims).
      <ul>
      <li> A claim should be a single well-formed sentence. It should end with a period; it should follow correct capitalization of entity names (e.g. `India', not `india'); numbers can be formatted in any appropriate English format (including as words for smaller quantities).
      <li> A claim based on a table highlight should combine information of multiple cells if possible.
      <li> A claim based on highlighted sentences should not simply paraphrase a highlighted sentence or concatenate sentences.
      <li> Generated claims must not be subjective and be verifiable using publicly available information/knowledge.
      <li> The claim should be as unambiguous as possible and avoid vague or speculative language (e.g. might be, may be, could be, rarely, many, barely or other indeterminate count words)
      <li> The claim should directly reference entities (i.e. no pronouns or nominals)
      <li>Claims should not be about contemporary political topics
      "></button>
      <span class="box-label">Claim using highlight:</span>
      <input type="text"  spellcheck="true" class='generated-claim' id='generated-claim' size='70em' value="">
      <label for="claim-annotation-challenge-selector">Challenge:</label>
      <select id="claim-annotation-challenge-selector" class="selectpicker" multiple>
        <option value="Evidence Retrieval" data-content='<span data-toggle="tooltip" data-placement="right" title="A challenge to verify the claim will be the retrieval of required evidence.">Evidence Retrieval</span>'>Evidence Retrieval</option>
          <option value="Multi-hop Reasoning" data-content='<span data-toggle="tooltip" data-placement="right" title="Multi-hop reasoning will be a challenge for verifying that claim, i.e. several documents will be required for verification.">Multi-hop Reasoning</span>'>Multi-hop Reasoning</option>
          <option value="Commonsense Reasoning" data-content='<span data-toggle="tooltip" data-placement="right" title="Commonsense Reasoning will be a challenge for verifying that claim, i.e. knowledge that is commonly assumed to be known but probably hard to find on Wikipedia.">Commonsense Reasoning</span>'>Commonsense Reasoning</option>
        <option value="Linguistic Inference" data-content='<span data-toggle="tooltip" data-placement="right" title="The inference on textual information required to verify the claim will be a challenge.">Linguistic Inference</span>'>Linguistic Inference</option>
        <option value="Numerical Reasoning" data-content='<span data-toggle="tooltip" data-placement="right" title=" Numerical reasoning required to verify the claim will be a challenge, i.e. reasoning that involves numbers or arithmetic calculations.">Numerical Reasoning</span>'>Numerical Reasoning</option>
        <option value="Reasoning over Structure" data-content='<span data-toggle="tooltip" data-placement="right" title="Reasoning over Table or List(s) is a challenge due to complex reasoning on tables or due to the combining much information.">Reasoning over Structure</span>'>Reasoning over Structure</option>
      <option value="Combining List/Table and Text" data-content='<span data-toggle="tooltip" data-placement="right" title="Combining information from either List or Table(s) with Text is required and it could pose a challenge (e.g. combining a table and the page title is most likely not a challenge)">Combining List/Table and Text</span>'>Combining List/Table and Text</option>
        <option value="None" data-content='<span data-toggle="tooltip" data-placement="right" title="My Tooltip Title">None'>None</option>
      </select>
      <button type="button" class="btn btn-sm btn-info small h-5 fa fa-info rounded-circle"  data-html="true"  data-toggle="popover" title="Expected Verification Challenges" data-content=	"We are interested in gaining more insights into what challenges the claim annotators expect to exist for finding evidence for the claims they created. You can select one or multiple of the given challenge categories and also add your own terms.
      <ul>
      <li><b>Evidence Retrieval</b> A challenge to verify the claim will be the retrieval of required evidence </li>
      <li><b>Multi-hop Reasoning</b>  Multi-hop reasoning will be a challenge for verifying that claim, i.e. several documents will be required for verification. </li>
      <li><b>Commonsense Reasoning</b> Commonsense Reasoning will be a challenge for verifying that claim, i.e. knowledge that is commonly assumed to be known but probably hard to find on Wikipedia. </li>
      <li><b>Linguistic inference</b> The inference on textual information required to verify the claim will be a challenge. </li>
      <li><b>Numerical reasoning</b> Numerical reasoning required to verify the claim will be a challenge, i.e. reasoning that involves numbers or arithmetic calculations. </li>
      <li><b>Reasoning over structure</b> Reasoning over Table or List(s) is a challenge due to complex reasoning on tables or due to the combining much information.</li>
      <li><b> Combining List/Table and Text</b>  Combining information from either List or Table(s) with Text is required and it could pose a challenge (e.g. combining a table and the page title is most likely not a challenge). </li>
      <li><b> None </b> If no particular challenge can be identified. If unsure whether to select None or another label, always select the latter. </li>
      "></button>
      <br>
      <br>
      <button type="button" class="btn btn-sm btn-info small h-5 fa fa-info rounded-circle"  data-html="true" data-toggle="popover" data-content="The second claim should be based on the highlight, but must include information beyond the highlighted table/sentences. <ul>
        <li> <b> Same page </b>: Include information outside of the highlight but on the same page.
        <li> <b> Multiple pages </b>: Include information from other wikipedia page(s). You can search freely through Wikipedia using the search function and use available hyperlinks on the pages.
        </ul>
       You are free in deciding to modify the previously created claim that uses only the highlight or to create an unrelated one (that still includes information from the highlight)."></button>
      <span  id='multiple-pages' class="box-label">Not specified.</span>
      <input type="text" spellcheck="true"  class='generated-claim-extended' id='generated-claim-extended' size='70em' value="">
      <label for="claim-annotation-challenge-selector-extended">Challenge:</label>
      <select id="claim-annotation-challenge-selector-extended" class="selectpicker" multiple>
        <option value="Evidence Retrieval" data-content='<span data-toggle="tooltip" data-placement="right" title="A challenge to verify the claim will be the retrieval of required evidence.">Evidence Retrieval</span>'>Evidence Retrieval</option>
          <option value="Multi-hop Reasoning" data-content='<span data-toggle="tooltip" data-placement="right" title="Multi-hop reasoning will be a challenge for verifying that claim, i.e. several documents will be required for verification.">Multi-hop Reasoning</span>'>Multi-hop Reasoning</option>
          <option value="Commonsense Reasoning" data-content='<span data-toggle="tooltip" data-placement="right" title="Commonsense Reasoning will be a challenge for verifying that claim, i.e. knowledge that is commonly assumed to be known but probably hard to find on Wikipedia.">Commonsense Reasoning</span>'>Commonsense Reasoning</option>
        <option value="Linguistic Inference" data-content='<span data-toggle="tooltip" data-placement="right" title="The inference on textual information required to verify the claim will be a challenge.">Linguistic Inference</span>'>Linguistic Inference</option>
        <option value="Numerical Reasoning" data-content='<span data-toggle="tooltip" data-placement="right" title=" Numerical reasoning required to verify the claim will be a challenge, i.e. reasoning that involves numbers or arithmetic calculations.">Numerical Reasoning</span>'>Numerical Reasoning</option>
        <option value="Reasoning over Structure" data-content='<span data-toggle="tooltip" data-placement="right" title="Reasoning over Table or List(s) is a challenge due to complex reasoning on tables or due to the combining much information.">Reasoning over Structure</span>'>Reasoning over Structure</option>
      <option value="Combining List/Table and Text" data-content='<span data-toggle="tooltip" data-placement="right" title="Combining information from either List or Table(s) with Text is required and it could pose a challenge (e.g. combining a table and the page title is most likely not a challenge)">Combining List/Table and Text</span>'>Combining List/Table and Text</option>
        <option value="None" data-content='<span data-toggle="tooltip" data-placement="right" title="My Tooltip Title">None'>None</option>
      </select>
      <br>
      <br>
      <button type="button" class="btn btn-sm btn-info small h-5 fa fa-info rounded-circle" data-toggle="popover" data-html="true" data-content="Modify the specified claim with the shown mutations type: <br> <ul> <li> <b> More Specific</b>: Make the claim more specific so that the new claim implies the original claim (by making the meaning more specific).
      <li> <b> Generalization </b>: Make the claim more general so that the new claim can be implied by the original claim (by making the meaning less specific)
      <li> <b> Negation </b>: Negate the meaning of the claim.
      <li> <b> Multiple Pages </b>: Incorporate information from multiple Wikipedia articles into the claim.
      <li> <b> Paraphrasing </b>: Rephrase the claim so that it has the same meaning
      <li> <b> Entity Substitution </b>: Substitute an entity in the claim to alternative from either the same or a different set of things.
      </ul>"></button>
      <span id='manipulations' class="box-label">Not specified. </span>
      <input type="text" spellcheck="true"  class='generated-claim-manipulation' id='generated-claim-manipulation' size='70em' value="">
      <label for="claim-annotation-challenge-selector-manipulation">Challenge:</label>
      <select id="claim-annotation-challenge-selector-manipulation" class="selectpicker" multiple>
        <option value="Evidence Retrieval" data-content='<span data-toggle="tooltip" data-placement="right" title="A challenge to verify the claim will be the retrieval of required evidence.">Evidence Retrieval</span>'>Evidence Retrieval</option>
          <option value="Multi-hop Reasoning" data-content='<span data-toggle="tooltip" data-placement="right" title="Multi-hop reasoning will be a challenge for verifying that claim, i.e. several documents will be required for verification.">Multi-hop Reasoning</span>'>Multi-hop Reasoning</option>
          <option value="Commonsense Reasoning" data-content='<span data-toggle="tooltip" data-placement="right" title="Commonsense Reasoning will be a challenge for verifying that claim, i.e. knowledge that is commonly assumed to be known but probably hard to find on Wikipedia.">Commonsense Reasoning</span>'>Commonsense Reasoning</option>
        <option value="Linguistic Inference" data-content='<span data-toggle="tooltip" data-placement="right" title="The inference on textual information required to verify the claim will be a challenge.">Linguistic Inference</span>'>Linguistic Inference</option>
        <option value="Numerical Reasoning" data-content='<span data-toggle="tooltip" data-placement="right" title=" Numerical reasoning required to verify the claim will be a challenge, i.e. reasoning that involves numbers or arithmetic calculations.">Numerical Reasoning</span>'>Numerical Reasoning</option>
        <option value="Reasoning over Structure" data-content='<span data-toggle="tooltip" data-placement="right" title="Reasoning over Table or List(s) is a challenge due to complex reasoning on tables or due to the combining much information.">Reasoning over Structure</span>'>Reasoning over Structure</option>
      <option value="Combining List/Table and Text" data-content='<span data-toggle="tooltip" data-placement="right" title="Combining information from either List or Table(s) with Text is required and it could pose a challenge (e.g. combining a table and the page title is most likely not a challenge)">Combining List/Table and Text</span>'>Combining List/Table and Text</option>
        <option value="None" data-content='<span data-toggle="tooltip" data-placement="right" title="My Tooltip Title">None'>None</option>
      </select>
      <br>
  </div>

<div id="submission-buttons">
  <button type='button' class="fa fa-undo btn btn-secondary" id='generated-claim-return'> Jump to Highlight</button>
  <button type='button' class="fa fa-check btn btn-success" id='generated-claim-submit'> Submit Claims</button>
</div>

</div>
<!-- <script async src="https://cse.google.com/cse.js?cx=cbebfba8d476ba4dc"></script>
<div class="gcse-search"></div> -->
</body>
</html>

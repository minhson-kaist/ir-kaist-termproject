# Google Natural Questions Documentation #

## Keys ##
1. annotations
2. document_html
3. document_title
4. document_tokens
5. document_url
6. example_id
7. long_answer_candidates
8. question_text
9. question_tokens

## Inside values ##

### annotation ###
> annotation_id

> long_answer: 
* candidate_index
* end_byte
* end_token 
* start_byte
* start_token.
>short_answers: 
* end_byte
* end_token
* start_byte
* start_token.
>yes_no_answer 

### document_html ###

> HTML file of the Wikipedia article.

### document_title ###
>Title of the document.

### document_tokens ###
>Individual words in the article, including HTML tokens like: `<H1>`, `<Table>`, ...

### document_url ###
>The link to the Wikipedia page which contains the article.

### example_id ###
>ID of the article

### long_answer_candidates ###
>A list of dictionaries, each dictionary contains 4 components: `end_byte`, `end_token`, `start_byte`, `start_token` and another ***boolean*** component: `top_level`.

### question_text ###
>Full text of the question. For example: 

>`when is the last episode of season 8 of the walking dead` 

### question_tokens ###
>List of tokens appeared in the question. For example:

>`['when', 'is', 'the', 'last', 'episode', 'of', 'season', '8', 'of', 'the', 'walking', 'dead']`

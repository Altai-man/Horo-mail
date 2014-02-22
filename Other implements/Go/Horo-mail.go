package main

import (
	"fmt" // For output testing.
	"io/ioutil" // For reading and writing.
	"log"       // Log as usual,
	"net/http"  // For downloading page source.
	"regexp"     // For parsing text.
	"strings"   // For replace method.
)

func get_page() string {
	// At first we get response from page.
	res, err := http.Get("http://www.horochan.ru")
	// Chech error free...
	if err != nil {
		log.Fatal(err)
	}
	// ReadAll text from body of source.
	raw_source, err := (ioutil.ReadAll(res.Body))
	res.Body.Close()
	if err != nil {
		log.Fatal(err)
	}
	//  write whole the body of raw_source...
	err = ioutil.WriteFile("source_file", raw_source, 0644)
	// What the hack is 0644?
	if err != nil {
		panic(err)
	}
	return string(raw_source)
}

func parsing(source string) []string  {
	// Splitting and getting last post.
	array_str := strings.Split(source, "<!-- REPLY CONTAINER -->")
	source = array_str[1]

	source = strings.Replace(source, "\"", "_", -1)
	// Work ONLY while count of posts lower than 99999. To rewrite properly.
	PATTERN_POST_NUM, err := regexp.Compile("[0-9][0-9][0-9][0-9][0-9]") 
	if err != nil { log.Fatal(err) }
	PATTERN_BOARD, err := regexp.Compile("/[abd]/")
	if err != nil { log.Fatal(err) }
	PATTERN_THREAD, err := regexp.Compile("/[0-9][0-9][0-9][0-9][0-9]/")
	if err != nil { log.Fatal(err) }
	PATTERN_TEXT, err := regexp.Compile("(?s)<div class=_message_>.*?</div>")
	if err != nil { log.Fatal(err) }
	PATTERN_PIC, err := regexp.Compile("http://.*?.jpg")
	if err != nil { log.Fatal(err) }

	board := PATTERN_BOARD.FindString(source)
	post_number := PATTERN_POST_NUM.FindString(source)

	thread := PATTERN_THREAD.FindString(source)
	thread = strings.Replace(thread, "/", "", -1)

	text := PATTERN_TEXT.FindString(source)
	text = strings.Replace(text, "<div class=_message_>", "", -1)
	text = strings.Replace(text, "</div>", "", -1)
	text = strings.Replace(text, "\n", "", 1)
	text = strings.Replace(text, "\t", "", -1)
	// TODO >> as links.

	pic_link := PATTERN_PIC.FindString(source)

	fmt.Println(source)
	parsed := []string{post_number, board, thread, text, pic_link}
	return parsed
}

func main() {
	// Get raw HTML-page.
	raw_source := get_page()
	// Parsing.
	parsed := parsing(raw_source)
	// Assignments.
	post_number := parsed[0]
	board := parsed[1]
	thread := parsed[2]
	text := parsed[3]
	pic_link := parsed[4]
	fmt.Println(post_number)
	fmt.Println(board)
	fmt.Println(thread)
	fmt.Println(text)
	fmt.Println(pic_link)
}

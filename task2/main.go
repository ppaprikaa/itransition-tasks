package main

import (
	"fmt"
	"log"
	"os"
	"sort"
	"strings"

	"golang.org/x/crypto/sha3"
)

const (
	dirPath = "data"
)

func main() {
	email := os.Args[1:][0]
	sha256hashes, err := generateSHA3_256ForEachFile(dirPath)
	if err != nil {
		log.Fatal(err)
	}

	hexArr := Bytes32ToHexAndHashStrings(sha256hashes...)
	sort.Strings(hexArr)

	hashes := strings.Join(hexArr, "")

	hashes = strings.Join([]string{hashes, email}, " ")

	hash := fmt.Sprintf("%x", sha3.Sum256([]byte(hashes)))
	fmt.Println(hash)
	fmt.Println(len([]rune(hash)))
}

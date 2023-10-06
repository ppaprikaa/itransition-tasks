package main

import (
	"fmt"
	"log"
	"sort"
	"strings"

	"golang.org/x/crypto/sha3"
)

const (
	dirPath = "data"
)

func main() {
	sha256hashes, err := generateSHA3_256ForEachFile(dirPath)
	if err != nil {
		log.Fatal(err)
	}

	hexArr := Bytes32ToHexAndHashStrings(sha256hashes...)
	sort.Strings(hexArr)

	hashes := strings.Join(hexArr, "")

	hashes = strings.Join([]string{hashes, "sanzhar.maratov@proton.me"}, " ")

	hash := fmt.Sprintf("%x", sha3.Sum256([]byte(hashes)))
	fmt.Println(hash)
	fmt.Println(len([]rune(hash)))
}

package main

import (
	"fmt"
	"os"
	"path/filepath"

	"golang.org/x/crypto/sha3"
)

func generateSHA3_256ForEachFile(dirPath string) ([][32]byte, error) {
	var (
		res = make([][32]byte, 0)
	)

	dir, err := os.ReadDir(dirPath)
	if err != nil {
		return nil, err
	}

	for _, dirEntry := range dir {
		fileData, err := os.ReadFile(filepath.Join(dirPath, dirEntry.Name()))
		if err != nil {
			return nil, err
		}

		dataHash := sha3.Sum256(fileData)

		res = append(res, dataHash)
	}

	return res, nil
}

func Bytes32ToHexAndHashStrings(bytesArr ...[32]byte) []string {
	var (
		result = make([]string, len(bytesArr))
	)

	for _, bytes := range bytesArr {
		result = append(result, fmt.Sprintf("%x", bytes[:]))
	}

	return result
}

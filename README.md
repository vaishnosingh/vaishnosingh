<div align="center">

  <!-- ANIMATED CYBER HEADER -->
  <img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=0:090D16,50:1E293B,100:0EA5E9&height=210&section=header&text=Vaishno%20Kumar%20Singh&fontSize=48&fontColor=ffffff&animation=fadeIn&fontAlignY=36&desc=AI%20%26%20Machine%20Learning%20%E2%80%A2%20Golang%20%26%20Python%20Backend%20Systems&descAlignY=58&descSize=17" alt="Header" />

  <!-- LIVE TYPING MOTION GRAPHIC -->
  <a href="https://git.io/typing-svg">
    <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=19&duration=2600&pause=900&color=38BDF8&center=true&vCenter=true&repeat=true&width=780&height=45&lines=%3E+Working+on+Python%2C+Deep+Learning+%26+Computer+Vision;%3E+Currently+Learning+Golang%2C+Django+%26+TensorFlow;%3E+Engineering+Low-Latency+APIs+with+FastAPI%2C+PostgreSQL+%26+ScyllaDB;%3E+Ask+me+about+Python%2C+Golang+%26+Data+Structures+and+Algorithms" alt="Typing SVG" />
  </a>

  <br><br>

  <!-- SOCIAL LINKS (NO UNDERLINE ARTIFACTS) -->
  <p align="center">
    <a href="https://www.linkedin.com/in/vshnsngh333" target="_blank"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" /></a>&nbsp;
    <a href="https://www.codechef.com/users/vshn_sngh" target="_blank"><img src="https://img.shields.io/badge/CodeChef-5B4638?style=for-the-badge&logo=codechef&logoColor=white" alt="CodeChef" /></a>&nbsp;
    <a href="https://www.hackerrank.com/profile/vaishnosingh9" target="_blank"><img src="https://img.shields.io/badge/HackerRank-00EA64?style=for-the-badge&logo=HackerRank&logoColor=black" alt="HackerRank" /></a>&nbsp;
    <a href="https://instagram.com/vshnsngh" target="_blank"><img src="https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white" alt="Instagram" /></a>&nbsp;
    <a href="mailto:vaishnosingh9@gmail.com"><img src="https://img.shields.io/badge/vaishnosingh9@gmail.com-EA4335?style=for-the-badge&logo=gmail&logoColor=white" alt="Gmail" /></a>
  </p>

</div>

---

### ⚡ `whoami`

```go
package main

import "fmt"

type Developer struct {
	Name         string
	Location     string
	WorkingOn    []string
	Learning     []string
	Architecture []string
	FunFact      string
}

func main() {
	vaishno := Developer{
		Name:         "Vaishno Kumar Singh",
		Location:     "India 🇮🇳",
		WorkingOn:    []string{"Python", "Artificial Intelligence", "Machine Learning", "DSA"},
		Learning:     []string{"Golang", "Django", "TensorFlow"},
		Architecture: []string{"FastAPI", "ScyllaDB", "PostgreSQL", "Linux"},
		FunFact:      "I think I am funny 🌝",
	}
	fmt.Printf("⚡ Initialized: %s\n", vaishno.Name)
}

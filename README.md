<!-- ANIMATED HEADER BANNER -->
<div align="center">
  <img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=12,14,19,24&height=200&section=header&text=Vaishno%20Kumar%20Singh&fontSize=46&fontColor=ffffff&animation=fadeIn&fontAlignY=35&desc=AI%2FML%20Engineer%20%E2%80%A2%20Golang%20%26%20Python%20Backend%20Architect&descAlignY=58&descSize=17" alt="Header Banner" />

  <!-- TRANSPARENT ANIMATED TYPING SVG -->
  <a href="https://git.io/typing-svg">
    <img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=600&size=20&duration=2800&pause=1000&color=38BDF8&center=true&vCenter=true&repeat=true&width=750&height=45&lines=Architecting+Intelligent+Systems+with+Python%2C+PyTorch+%26+TensorFlow;Building+Ultra-Low-Latency+APIs+in+Golang%2C+FastAPI+%26+Django;Scaling+Data+Layers+on+ScyllaDB%2C+PostgreSQL+%26+Linux" alt="Typing SVG" />
  </a>

  <!-- SOCIAL & PROFILE BADGES -->
  <p align="center">
    <a href="https://www.linkedin.com/in/vshnsngh333" target="_blank" rel="noreferrer">
      <img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" />
    </a>
    <a href="https://www.codechef.com/users/vshn_sngh" target="_blank" rel="noreferrer">
      <img src="https://img.shields.io/badge/CodeChef-5B4638?style=for-the-badge&logo=codechef&logoColor=white" alt="CodeChef" />
    </a>
    <a href="https://www.hackerrank.com/profile/vaishnosingh9" target="_blank" rel="noreferrer">
      <img src="https://img.shields.io/badge/HackerRank-00EA64?style=for-the-badge&logo=HackerRank&logoColor=black" alt="HackerRank" />
    </a>
    <a href="https://instagram.com/vshnsngh" target="_blank" rel="noreferrer">
      <img src="https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white" alt="Instagram" />
    </a>
    <a href="mailto:vaishnosingh9@gmail.com">
      <img src="https://img.shields.io/badge/Gmail-EA4335?style=for-the-badge&logo=gmail&logoColor=white" alt="Gmail" />
    </a>
    <img src="https://komarev.com/ghpvc/?username=vshn-sngh&label=Profile%20Views&color=38BDF8&style=for-the-badge" alt="Profile Views" />
  </p>
</div>

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%" alt="Divider" />

### ⚡ `<AboutMe />`

```go
package main

import "fmt"

type Engineer struct {
	Name      string
	Role      string
	Location  string
	Focus     []string
	Learning  []string
	Databases []string
	FunFact   string
}

func main() {
	vks := Engineer{
		Name:      "Vaishno Kumar Singh",
		Role:      "AI/ML & Backend Systems Developer",
		Location:  "India 🇮🇳",
		Focus:     []string{"Python", "Deep Learning", "FastAPI", "DSA"},
		Learning:  []string{"Golang", "Django", "TensorFlow"},
		Databases: []string{"ScyllaDB", "PostgreSQL", "MySQL", "MariaDB"},
		FunFact:   "I think I am funny 🌝",
	}
	fmt.Printf("⚡ Ready to scale: %s (%s)\n", vks.Name, vks.Role)
}

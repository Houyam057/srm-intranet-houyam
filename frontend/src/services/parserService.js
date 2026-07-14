// src/services/parserService.js
class ParserService {
  parse(ocrResult, filename) {
    const { text = "" } = ocrResult;
    const cleanText = text.replace(/En savoir plus →|logo|SRM|TTA/gi, "").trim();

    const lines = cleanText.split('\n').map(l => l.trim()).filter(l => l.length > 3);
    const hasArabic = /[\u0600-\u06FF]/.test(cleanText);

    return {
      id: filename.replace(".png", ""),
      image: `/flashinfos/${filename}`,
      
      // Date : toujours "Avril 2026" par défaut comme tu veux
      date: this.extractDate(cleanText) || "Avril 2026",

      title: this.extractTitle(lines, hasArabic),
      summary: this.extractSummary(lines),
    };
  }

  extractDate(text) {
    // Détection stricte sans valeur par défaut "Avril"
    const match = text.match(/(?:Avril|Mai|Juin|Juillet|Août|Septembre|Octobre|Novembre|Décembre|إبريل|ابريل)\s*202[0-9]/i);
    
    if (match) {
      return match[0];
    }

    // Recherche simple de mois seul
    if (/Mai/i.test(text)) return "Mai 2026";
    if (/Juin/i.test(text)) return "Juin 2026";
    if (/إبريل|ابريل/i.test(text)) return "إبريل 2026";
    if (/Avril/i.test(text)) return "Avril 2026";

    return "";   // Plus de valeur par défaut forcée
  }

  extractTitle(lines, hasArabic) {
    return "Flash Info SRM-TTA - موجه إخباري";
  }

  extractSummary(lines) {
    let summary = [];
    for (const line of lines.slice(1, 8)) {
      if (line.length > 25) {
        summary.push(line);
        if (summary.length >= 3) break;
      }
    }
    return summary.join(" ").substring(0, 220) || "Résumé du flash info...";
  }
}

export default new ParserService();
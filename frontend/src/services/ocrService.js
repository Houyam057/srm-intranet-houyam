// src/services/ocrService.js
import Tesseract from "tesseract.js";

class OCRService {
  async extract(imagePath) {
    try {
      console.log(`🔍 OCR démarré : ${imagePath}`);

      const worker = await Tesseract.createWorker("fra+ara+eng", 1, {
        logger: (m) => {
          if (m.status === "recognizing text") {
            console.log(`OCR ${Math.round(m.progress * 100)}% - ${imagePath}`);
          }
        }
      });

      const { data } = await worker.recognize(imagePath, {
        tessedit_pageseg_mode: "3",
      });

      await worker.terminate();

      console.log(`✅ OCR terminé pour ${imagePath} (${data.text.length} caractères)`);
      return { text: data.text, words: data.words || [] };

    } catch (error) {
      console.error(`❌ OCR échoué pour ${imagePath}`, error);
      return { text: "", words: [] };
    }
  }
}

export default new OCRService();
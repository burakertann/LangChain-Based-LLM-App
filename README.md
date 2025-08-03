# LangChain-Based-LLM App

LangChain tabanlı bu uygulama, kullanıcıdan gelen soruları önce yerel doküman havuzunda arar. Eğer yeterli bilgi bulunamazsa, otomatik olarak web araması yaparak güncel verilerle yanıt üretir.

## 🔍 Özellikler

- 📁 Yerel dokümanlardan bilgi çekme (RAG)
- 🌐 Gerekirse web araması yapma
- 💬 Kullanıcıyla doğal dilde sohbet
- ⚙️ LangChain ile esnek ve genişletilebilir yapı

## 🚀 Kurulum

```bash
git clone https://github.com/kullaniciadi/langchain-based-llm-app.git
cd langchain-based-llm-app
python -m venv venv
source venv/bin/activate  # Windows için: venv\Scripts\activate
pip install -r requirements.txt

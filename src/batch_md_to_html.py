import markdown
import os
from datetime import datetime

def get_css_styles(template_style):
    """
    Get CSS styles for different template styles based on sample_630.html design
    """
    css_styles = {
        "professional": """
        /* Professional Business Style - Complete sample_630.html Implementation */
        :root {
            --primary: #3a86ff;
            --primary-dark: #0048b3;
            --secondary: #00bfff;
            --success: #22c55e;
            --warning: #f59e0b;
            --danger: #ef4444;
            --info: #0ea5e9;
            --tech: #9333ea;
            --practical: #ec4899;
            --text: #2d3748;
            --text-light: #475569;
            --text-lighter: #94a3b8;
            --bg: #f0f4f8;
            --card: #fff;
            --border: #e2e8f0;
            --shadow-sm: 0 4px 12px rgba(0, 0, 0, 0.05);
            --shadow-md: 0 10px 25px rgba(0, 0, 0, 0.07);
            --shadow-lg: 0 15px 35px rgba(0, 0, 0, 0.1);
            --transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
            --radius-sm: 8px;
            --radius-md: 12px;
            --radius-lg: 16px;
        }

        @media (prefers-color-scheme: dark) {
            :root {
                --primary: #4b93ff;
                --primary-dark: #2f6bff;
                --secondary: #33c5ff;
                --success: #3dd16e;
                --warning: #fba024;
                --danger: #f55656;
                --info: #22b3fb;
                --tech: #a251f7;
                --practical: #f16dac;
                --text: #e2e8f0;
                --text-light: #cbd5e1;
                --text-lighter: #94a3b8;
                --bg: #121825;
                --card: #1e293b;
                --border: #334155;
                --shadow-sm: 0 4px 12px rgba(0, 0, 0, 0.2);
                --shadow-md: 0 10px 25px rgba(0, 0, 0, 0.25);
                --shadow-lg: 0 15px 35px rgba(0, 0, 0, 0.3);
            }
        }

        * {
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', 'Roboto', 'Microsoft JhengHei', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: var(--bg);
            color: var(--text);
            margin: 0;
            padding: 0;
            line-height: 1.7;
            overflow-x: hidden;
        }
        
        .container {
            max-width: 1000px;
            margin: 40px auto;
            padding: 0 24px;
        }
        
        header {
            text-align: center;
            padding: 60px 30px;
            background: linear-gradient(135deg, var(--primary), var(--primary-dark));
            color: #fff;
            position: relative;
            box-shadow: var(--shadow-lg);
            border-radius: var(--radius-lg) var(--radius-lg) 0 0;
            overflow: hidden;
        }
        
        header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-image: url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M11 18c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm48 25c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm-43-7c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm63 31c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM34 90c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm56-76c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM12 86c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm28-65c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm23-11c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-6 60c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm29 22c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zM32 63c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm57-13c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-9-21c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM60 91c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM35 41c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM12 60c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2z' fill='%23ffffff' fill-opacity='0.05' fill-rule='evenodd'/%3E%3C/svg%3E");
            opacity: 0.6;
            z-index: 0;
        }
        
        header h1 {
            font-size: 2.4rem;
            margin: 0 0 16px 0;
            letter-spacing: 0.5px;
            font-weight: 800;
            position: relative;
            z-index: 1;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        
        header p {
            font-size: 1.2rem;
            margin: 0;
            opacity: 0.95;
            position: relative;
            z-index: 1;
            max-width: 700px;
            margin: 0 auto;
        }
        
        .content {
            background-color: var(--card);
            border-radius: 0 0 var(--radius-lg) var(--radius-lg);
            box-shadow: var(--shadow-lg);
            padding: 40px;
            margin-bottom: 40px;
            position: relative;
        }
        
        .content::after {
            content: '';
            position: absolute;
            bottom: -10px;
            left: 5%;
            right: 5%;
            height: 10px;
            background-color: rgba(0, 0, 0, 0.03);
            border-radius: 50%;
            filter: blur(8px);
            z-index: -1;
        }
        
        /* 基礎區塊樣式 - Based on sample_630.html */
        .section-block {
            background-color: var(--card);
            padding: 35px;
            border-radius: var(--radius-lg);
            margin-bottom: 40px;
            border-left: 5px solid var(--primary);
            box-shadow: var(--shadow-md);
            transition: var(--transition);
            position: relative;
            overflow: hidden;
        }
        
        .section-block::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--primary) 0%, var(--secondary) 50%, #00d1b2 100%);
            opacity: 0.8;
        }
        
        .section-block:hover {
            transform: translateY(-8px);
            box-shadow: 0 20px 30px rgba(0, 0, 0, 0.1);
        }
        
        /* 會議資訊區塊 */
        .section-block.meeting-info {
            border-left-color: var(--secondary);
            background: linear-gradient(135deg, #f0f7ff 0%, #e1f5fe 100%);
        }
        
        .section-block.meeting-info::before {
            background: linear-gradient(90deg, var(--secondary) 0%, #0091ea 100%);
        }
        
        /* 內容章節區塊 */
        .section-block.content-section {
            border-left-color: #00d1b2;
            background: linear-gradient(135deg, #f0fff4 0%, #e0f2f1 100%);
        }
        
        .section-block.content-section::before {
            background: linear-gradient(90deg, #00d1b2 0%, #00b894 100%);
        }
        
        /* 技術背景區塊 */
        .section-block.tech-background {
            border-left-color: var(--tech);
            background: linear-gradient(135deg, #f5f3ff 0%, #ede9fe 100%);
        }
        
        .section-block.tech-background::before {
            background: linear-gradient(90deg, var(--tech) 0%, #6d28d9 100%);
        }
        
        /* 核心觀點區塊 */
        .section-block.core-insights {
            border-left-color: var(--warning);
            background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
        }
        
        .section-block.core-insights::before {
            background: linear-gradient(90deg, var(--warning) 0%, #d97706 100%);
        }
        
        /* 實踐經驗區塊 */
        .section-block.practical-experience {
            border-left-color: var(--practical);
            background: linear-gradient(135deg, #fdf2f8 0%, #fce7f3 100%);
        }
        
        .section-block.practical-experience::before {
            background: linear-gradient(90deg, var(--practical) 0%, #db2777 100%);
        }
        
        /* 區塊標題樣式 - Based on sample_630.html */
        .section-title {
            font-size: 1.75rem;
            margin-top: 0;
            margin-bottom: 30px;
            padding-bottom: 16px;
            border-bottom: 3px solid var(--primary);
            display: flex;
            align-items: center;
            color: var(--primary);
            font-weight: 800;
            position: relative;
            letter-spacing: -0.5px;
        }
        
        .section-title::before {
            content: '📋';
            margin-right: 14px;
            font-size: 1.3em;
            filter: drop-shadow(0 2px 3px rgba(0,0,0,0.1));
        }
        
        .section-block.meeting-info .section-title {
            color: var(--secondary);
            border-bottom-color: var(--secondary);
        }
        
        .section-block.meeting-info .section-title::before {
            content: '📊';
        }
        
        .section-block.content-section .section-title {
            color: #00d1b2;
            border-bottom-color: #00d1b2;
        }
        
        .section-block.content-section .section-title::before {
            content: '📝';
        }
        
        .section-block.tech-background .section-title {
            color: var(--tech);
            border-bottom-color: var(--tech);
        }
        
        .section-block.tech-background .section-title::before {
            content: '⚙️';
        }
        
        .section-block.core-insights .section-title {
            color: var(--warning);
            border-bottom-color: var(--warning);
        }
        
        .section-block.core-insights .section-title::before {
            content: '💡';
        }
        
        .section-block.practical-experience .section-title {
            color: var(--practical);
            border-bottom-color: var(--practical);
        }
        
        .section-block.practical-experience .section-title::before {
            content: '🛠️';
        }

        /* 響應式設計 - Based on sample_630.html */
        @media (max-width: 1200px) {
            .container {
                max-width: 95%;
                padding: 0 20px;
            }
        }

        @media (max-width: 768px) {
            body {
                font-size: 16px;
                padding: 0;
            }

            .container {
                margin: 20px auto;
                padding: 0 16px;
            }

            header {
                padding: 40px 20px;
                border-radius: var(--radius-md) var(--radius-md) 0 0;
            }

            header h1 {
                font-size: 2rem;
                margin-bottom: 12px;
            }

            header p {
                font-size: 1rem;
            }

            .content {
                padding: 30px 20px;
                border-radius: 0 0 var(--radius-md) var(--radius-md);
            }

            .section-block {
                padding: 25px 20px;
                margin-bottom: 30px;
            }

            .section-title {
                font-size: 1.5rem;
                margin-bottom: 24px;
            }
        }

        @media (max-width: 480px) {
            header {
                padding: 30px 16px;
            }

            header h1 {
                font-size: 1.8rem;
            }

            .content {
                padding: 24px 16px;
            }

            .section-block {
                padding: 20px 16px;
                margin-bottom: 24px;
            }

            .section-title {
                font-size: 1.3rem;
                margin-bottom: 20px;
            }
        }

        /* 統一的頁面頭部和頁腳圖標樣式 */
        header img {
            max-width: 35%;
            height: auto;
            margin-bottom: 20px;
            filter: drop-shadow(0 4px 12px rgba(0,0,0,0.15));
            transition: transform 0.5s ease;
            transform-origin: center;
        }

        header img:hover {
            transform: scale(1.05) rotate(2deg);
        }

        footer {
            text-align: center;
            padding: 40px 20px;
            background: linear-gradient(135deg, var(--primary), var(--primary-dark));
            color: #fff;
            border-radius: var(--radius-lg);
            position: relative;
            overflow: hidden;
            margin-top: 60px;
            box-shadow: var(--shadow-lg);
        }

        footer::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-image: url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M11 18c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm48 25c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm-43-7c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm63 31c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM34 90c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm56-76c1.657 0 3-1.343 3-3s-3.134-3-7-7-7 3.134-7 7 3.134 7 7 7zm48 25c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm-43-7c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm63 31c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM34 90c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm56-76c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM12 86c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm28-65c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm23-11c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-6 60c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm29 22c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zM32 63c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm57-13c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-9-21c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM60 91c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM35 41c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM12 60c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2z' fill='%23ffffff' fill-opacity='0.05' fill-rule='evenodd'/%3E%3C/svg%3E");
            opacity: 0.6;
            z-index: 0;
        }

        footer img {
            max-width: 35%;
            height: auto;
            margin-bottom: 20px;
            filter: drop-shadow(0 4px 12px rgba(0,0,0,0.15));
            position: relative;
            z-index: 1;
        }

        footer p {
            margin: 10px 0;
            opacity: 0.9;
            position: relative;
            z-index: 1;
            text-align: center;
            color: white;
        }
        """,

        "technical": """
        /* Technical Documentation Style - Complete sample_630.html Implementation */
        :root {
            --primary: #00d4aa;
            --primary-dark: #00a085;
            --secondary: #4fc3f7;
            --success: #4caf50;
            --warning: #ff9800;
            --danger: #f44336;
            --info: #2196f3;
            --tech: #9c27b0;
            --practical: #e91e63;
            --text: #e2e8f0;
            --text-light: #cbd5e1;
            --text-lighter: #94a3b8;
            --bg: #0f172a;
            --card: #1e293b;
            --border: #334155;
            --shadow-sm: 0 4px 12px rgba(0, 0, 0, 0.3);
            --shadow-md: 0 10px 25px rgba(0, 0, 0, 0.4);
            --shadow-lg: 0 15px 35px rgba(0, 0, 0, 0.5);
            --transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
            --radius-sm: 8px;
            --radius-md: 12px;
            --radius-lg: 16px;
        }

        * {
            box-sizing: border-box;
        }

        body {
            font-family: 'JetBrains Mono', 'Fira Code', 'Inter', 'Roboto', 'Microsoft JhengHei', monospace;
            background-color: var(--bg);
            color: var(--text);
            margin: 0;
            padding: 0;
            line-height: 1.7;
            overflow-x: hidden;
        }

        .container {
            max-width: 1000px;
            margin: 40px auto;
            padding: 0 24px;
        }

        header {
            text-align: center;
            padding: 60px 30px;
            background: linear-gradient(135deg, var(--primary), var(--primary-dark));
            color: #fff;
            position: relative;
            box-shadow: var(--shadow-lg);
            border-radius: var(--radius-lg) var(--radius-lg) 0 0;
            overflow: hidden;
        }

        header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-image: url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M11 18c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm48 25c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm-43-7c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm63 31c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM34 90c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm56-76c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM12 86c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm28-65c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm23-11c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-6 60c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm29 22c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zM32 63c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm57-13c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-9-21c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM60 91c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM35 41c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM12 60c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2z' fill='%23ffffff' fill-opacity='0.05' fill-rule='evenodd'/%3E%3C/svg%3E");
            opacity: 0.6;
            z-index: 0;
        }

        header h1 {
            font-size: 2.4rem;
            margin: 0 0 16px 0;
            letter-spacing: 0.5px;
            font-weight: 800;
            position: relative;
            z-index: 1;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }

        header p {
            font-size: 1.2rem;
            margin: 0;
            opacity: 0.95;
            position: relative;
            z-index: 1;
            max-width: 700px;
            margin: 0 auto;
        }

        .content {
            background-color: var(--card);
            border-radius: 0 0 var(--radius-lg) var(--radius-lg);
            box-shadow: var(--shadow-lg);
            padding: 40px;
            margin-bottom: 40px;
            position: relative;
        }

        .content::after {
            content: '';
            position: absolute;
            bottom: -10px;
            left: 5%;
            right: 5%;
            height: 10px;
            background-color: rgba(0, 0, 0, 0.03);
            border-radius: 50%;
            filter: blur(8px);
            z-index: -1;
        }

        /* 基礎區塊樣式 - Based on sample_630.html */
        .section-block {
            background-color: var(--card);
            padding: 35px;
            border-radius: var(--radius-lg);
            margin-bottom: 40px;
            border-left: 5px solid var(--primary);
            box-shadow: var(--shadow-md);
            transition: var(--transition);
            position: relative;
            overflow: hidden;
        }

        .section-block::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--primary) 0%, var(--secondary) 50%, #00d1b2 100%);
            opacity: 0.8;
        }

        .section-block:hover {
            transform: translateY(-8px);
            box-shadow: 0 20px 30px rgba(0, 0, 0, 0.1);
        }

        /* 會議資訊區塊 */
        .section-block.meeting-info {
            border-left-color: var(--secondary);
            background: linear-gradient(135deg, #0c1623 0%, #162032 100%);
        }

        .section-block.meeting-info::before {
            background: linear-gradient(90deg, var(--secondary) 0%, #0091ea 100%);
        }

        /* 內容章節區塊 */
        .section-block.content-section {
            border-left-color: #00d1b2;
            background: linear-gradient(135deg, #0f1a21 0%, #152b35 100%);
        }

        .section-block.content-section::before {
            background: linear-gradient(90deg, #00d1b2 0%, #00b894 100%);
        }

        /* 技術背景區塊 */
        .section-block.tech-background {
            border-left-color: var(--tech);
            background: linear-gradient(135deg, #191230 0%, #231942 100%);
        }

        .section-block.tech-background::before {
            background: linear-gradient(90deg, var(--tech) 0%, #6d28d9 100%);
        }

        /* 核心觀點區塊 */
        .section-block.core-insights {
            border-left-color: var(--warning);
            background: linear-gradient(135deg, #271b10 0%, #332211 100%);
        }

        .section-block.core-insights::before {
            background: linear-gradient(90deg, var(--warning) 0%, #d97706 100%);
        }

        /* 實踐經驗區塊 */
        .section-block.practical-experience {
            border-left-color: var(--practical);
            background: linear-gradient(135deg, #271019 0%, #331026 100%);
        }

        .section-block.practical-experience::before {
            background: linear-gradient(90deg, var(--practical) 0%, #db2777 100%);
        }

        /* 區塊標題樣式 - Based on sample_630.html */
        .section-title {
            font-size: 1.75rem;
            margin-top: 0;
            margin-bottom: 30px;
            padding-bottom: 16px;
            border-bottom: 3px solid var(--primary);
            display: flex;
            align-items: center;
            color: var(--primary);
            font-weight: 800;
            position: relative;
            letter-spacing: -0.5px;
        }

        .section-title::before {
            content: '⚡';
            margin-right: 14px;
            font-size: 1.3em;
            filter: drop-shadow(0 2px 3px rgba(0,0,0,0.1));
        }

        .section-block.meeting-info .section-title {
            color: var(--secondary);
            border-bottom-color: var(--secondary);
        }

        .section-block.meeting-info .section-title::before {
            content: '📊';
        }

        .section-block.content-section .section-title {
            color: #00d1b2;
            border-bottom-color: #00d1b2;
        }

        .section-block.content-section .section-title::before {
            content: '💻';
        }

        .section-block.tech-background .section-title {
            color: var(--tech);
            border-bottom-color: var(--tech);
        }

        .section-block.tech-background .section-title::before {
            content: '🔧';
        }

        .section-block.core-insights .section-title {
            color: var(--warning);
            border-bottom-color: var(--warning);
        }

        .section-block.core-insights .section-title::before {
            content: '🧠';
        }

        .section-block.practical-experience .section-title {
            color: var(--practical);
            border-bottom-color: var(--practical);
        }

        .section-block.practical-experience .section-title::before {
            content: '⚙️';
        }

        /* 統一的頁面頭部和頁腳圖標樣式 */
        header img {
            max-width: 35%;
            height: auto;
            margin-bottom: 20px;
            filter: drop-shadow(0 4px 12px rgba(0,0,0,0.15));
            transition: transform 0.5s ease;
            transform-origin: center;
        }

        header img:hover {
            transform: scale(1.05) rotate(2deg);
        }

        footer {
            text-align: center;
            padding: 40px 20px;
            background: linear-gradient(135deg, var(--primary), var(--primary-dark));
            color: #fff;
            border-radius: var(--radius-lg);
            position: relative;
            overflow: hidden;
            margin-top: 60px;
            box-shadow: var(--shadow-lg);
        }

        footer::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-image: url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M11 18c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm48 25c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm-43-7c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm63 31c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM34 90c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm56-76c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM12 86c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm28-65c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm23-11c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-6 60c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm29 22c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zM32 63c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm57-13c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-9-21c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM60 91c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM35 41c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM12 60c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2z' fill='%23ffffff' fill-opacity='0.05' fill-rule='evenodd'/%3E%3C/svg%3E");
            opacity: 0.6;
            z-index: 0;
        }

        footer img {
            max-width: 35%;
            height: auto;
            margin-bottom: 20px;
            filter: drop-shadow(0 4px 12px rgba(0,0,0,0.15));
            position: relative;
            z-index: 1;
        }

        footer p {
            margin: 10px 0;
            opacity: 0.9;
            position: relative;
            z-index: 1;
            text-align: center;
            color: white;
        }
        """,

        "concise": """
        /* Concise Summary Style - Complete sample_630.html Implementation */
        :root {
            --primary: #6366f1;
            --primary-dark: #4338ca;
            --secondary: #8b5cf6;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
            --info: #06b6d4;
            --tech: #8b5cf6;
            --practical: #ec4899;
            --text: #1e293b;
            --text-light: #475569;
            --text-lighter: #94a3b8;
            --bg: #f8fafc;
            --card: #fff;
            --border: #e2e8f0;
            --shadow-sm: 0 4px 12px rgba(0, 0, 0, 0.05);
            --shadow-md: 0 10px 25px rgba(0, 0, 0, 0.07);
            --shadow-lg: 0 15px 35px rgba(0, 0, 0, 0.1);
            --transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
            --radius-sm: 8px;
            --radius-md: 12px;
            --radius-lg: 16px;
        }

        @media (prefers-color-scheme: dark) {
            :root {
                --primary: #818cf8;
                --primary-dark: #6366f1;
                --secondary: #a78bfa;
                --success: #34d399;
                --warning: #fbbf24;
                --danger: #f87171;
                --info: #22d3ee;
                --tech: #a78bfa;
                --practical: #f472b6;
                --text: #e2e8f0;
                --text-light: #cbd5e1;
                --text-lighter: #94a3b8;
                --bg: #0f172a;
                --card: #1e293b;
                --border: #334155;
                --shadow-sm: 0 4px 12px rgba(0, 0, 0, 0.2);
                --shadow-md: 0 10px 25px rgba(0, 0, 0, 0.25);
                --shadow-lg: 0 15px 35px rgba(0, 0, 0, 0.3);
            }
        }

        * {
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', 'Roboto', 'Microsoft JhengHei', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: var(--bg);
            color: var(--text);
            margin: 0;
            padding: 0;
            line-height: 1.7;
            overflow-x: hidden;
        }

        .container {
            max-width: 1000px;
            margin: 40px auto;
            padding: 0 24px;
        }

        header {
            text-align: center;
            padding: 60px 30px;
            background: linear-gradient(135deg, var(--primary), var(--primary-dark));
            color: #fff;
            position: relative;
            box-shadow: var(--shadow-lg);
            border-radius: var(--radius-lg) var(--radius-lg) 0 0;
            overflow: hidden;
        }

        header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-image: url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M11 18c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm48 25c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm-43-7c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm63 31c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM34 90c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm56-76c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM12 86c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm28-65c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm23-11c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-6 60c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm29 22c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zM32 63c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm57-13c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-9-21c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM60 91c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM35 41c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM12 60c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2z' fill='%23ffffff' fill-opacity='0.05' fill-rule='evenodd'/%3E%3C/svg%3E");
            opacity: 0.6;
            z-index: 0;
        }

        header h1 {
            font-size: 2.4rem;
            margin: 0 0 16px 0;
            letter-spacing: 0.5px;
            font-weight: 800;
            position: relative;
            z-index: 1;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }

        header p {
            font-size: 1.2rem;
            margin: 0;
            opacity: 0.95;
            position: relative;
            z-index: 1;
            max-width: 700px;
            margin: 0 auto;
        }

        .content {
            background-color: var(--card);
            border-radius: 0 0 var(--radius-lg) var(--radius-lg);
            box-shadow: var(--shadow-lg);
            padding: 40px;
            margin-bottom: 40px;
            position: relative;
        }

        .content::after {
            content: '';
            position: absolute;
            bottom: -10px;
            left: 5%;
            right: 5%;
            height: 10px;
            background-color: rgba(0, 0, 0, 0.03);
            border-radius: 50%;
            filter: blur(8px);
            z-index: -1;
        }

        /* 基礎區塊樣式 - Based on sample_630.html */
        .section-block {
            background-color: var(--card);
            padding: 35px;
            border-radius: var(--radius-lg);
            margin-bottom: 40px;
            border-left: 5px solid var(--primary);
            box-shadow: var(--shadow-md);
            transition: var(--transition);
            position: relative;
            overflow: hidden;
        }

        .section-block::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--primary) 0%, var(--secondary) 50%, #00d1b2 100%);
            opacity: 0.8;
        }

        .section-block:hover {
            transform: translateY(-8px);
            box-shadow: 0 20px 30px rgba(0, 0, 0, 0.1);
        }

        /* 統一的頁面頭部和頁腳圖標樣式 */
        header img {
            max-width: 35%;
            height: auto;
            margin-bottom: 20px;
            filter: drop-shadow(0 4px 12px rgba(0,0,0,0.15));
            transition: transform 0.5s ease;
            transform-origin: center;
        }

        header img:hover {
            transform: scale(1.05) rotate(2deg);
        }

        footer {
            text-align: center;
            padding: 40px 20px;
            background: linear-gradient(135deg, var(--primary), var(--primary-dark));
            color: #fff;
            border-radius: var(--radius-lg);
            position: relative;
            overflow: hidden;
            margin-top: 60px;
            box-shadow: var(--shadow-lg);
        }

        footer img {
            max-width: 35%;
            height: auto;
            margin-bottom: 20px;
            filter: drop-shadow(0 4px 12px rgba(0,0,0,0.15));
            position: relative;
            z-index: 1;
        }

        footer p {
            margin: 10px 0;
            opacity: 0.9;
            position: relative;
            z-index: 1;
            text-align: center;
            color: white;
        }
        """,

        "presentation": """
        /* Presentation Style - Complete sample_630.html Implementation */
        :root {
            --primary: #e74c3c;
            --primary-dark: #c0392b;
            --secondary: #f39c12;
            --success: #27ae60;
            --warning: #f39c12;
            --danger: #e74c3c;
            --info: #3498db;
            --tech: #9b59b6;
            --practical: #e91e63;
            --text: #2c3e50;
            --text-light: #34495e;
            --text-lighter: #7f8c8d;
            --bg: linear-gradient(135deg, #e74c3c, #c0392b);
            --card: #fff;
            --border: #ecf0f1;
            --shadow-sm: 0 4px 12px rgba(0, 0, 0, 0.1);
            --shadow-md: 0 10px 25px rgba(0, 0, 0, 0.15);
            --shadow-lg: 0 15px 35px rgba(0, 0, 0, 0.2);
            --transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
            --radius-sm: 8px;
            --radius-md: 12px;
            --radius-lg: 16px;
        }

        * {
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', 'Roboto', 'Microsoft JhengHei', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--bg);
            color: var(--text);
            margin: 0;
            padding: 0;
            line-height: 1.7;
            min-height: 100vh;
            overflow-x: hidden;
        }

        .container {
            max-width: 1000px;
            margin: 40px auto;
            padding: 0 24px;
        }

        header {
            text-align: center;
            padding: 60px 30px;
            background: linear-gradient(135deg, var(--primary), var(--primary-dark));
            color: #fff;
            position: relative;
            box-shadow: var(--shadow-lg);
            border-radius: var(--radius-lg) var(--radius-lg) 0 0;
            overflow: hidden;
        }

        header h1 {
            font-size: 2.4rem;
            margin: 0 0 16px 0;
            letter-spacing: 0.5px;
            font-weight: 800;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
        }

        header p {
            font-size: 1.2rem;
            margin: 0;
            opacity: 0.95;
        }

        .content {
            background-color: var(--card);
            border-radius: 0 0 var(--radius-lg) var(--radius-lg);
            box-shadow: var(--shadow-lg);
            padding: 40px;
            margin-bottom: 40px;
        }

        /* 基礎區塊樣式 */
        .section-block {
            background-color: var(--card);
            padding: 35px;
            border-radius: var(--radius-lg);
            margin-bottom: 40px;
            border-left: 6px solid var(--primary);
            box-shadow: var(--shadow-md);
            transition: var(--transition);
            position: relative;
        }

        .section-block:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.15);
        }

        .section-block.meeting-info {
            border-left-color: var(--secondary);
            background: linear-gradient(135deg, #fff9e6 0%, #fff3d4 100%);
        }

        .section-block.content-section {
            border-left-color: var(--success);
            background: linear-gradient(135deg, #f0fff4 0%, #e6ffed 100%);
        }

        /* 統一的頁面頭部和頁腳圖標樣式 */
        header img {
            max-width: 35%;
            height: auto;
            margin-bottom: 20px;
            filter: drop-shadow(0 4px 12px rgba(0,0,0,0.15));
            transition: transform 0.5s ease;
            transform-origin: center;
        }

        header img:hover {
            transform: scale(1.05) rotate(2deg);
        }

        footer {
            text-align: center;
            padding: 40px 20px;
            background: linear-gradient(135deg, var(--primary), var(--primary-dark));
            color: #fff;
            border-radius: var(--radius-lg);
            position: relative;
            overflow: hidden;
            margin-top: 60px;
            box-shadow: var(--shadow-lg);
        }

        footer img {
            max-width: 35%;
            height: auto;
            margin-bottom: 20px;
            filter: drop-shadow(0 4px 12px rgba(0,0,0,0.15));
            position: relative;
            z-index: 1;
        }

        footer p {
            margin: 10px 0;
            opacity: 0.9;
            position: relative;
            z-index: 1;
            text-align: center;
            color: white;
        }
        """
    }

    return css_styles.get(template_style, css_styles["professional"])


def convert_markdown_to_html(markdown_content, template_style="professional", title="報告", subtitle="", header_image_path="", footer_image_path=""):
    """
    Convert markdown content to HTML with specified template style
    """
    # Convert markdown to HTML
    html_content = markdown.markdown(markdown_content, extensions=['tables', 'fenced_code'])

    # Get CSS styles
    css_styles = get_css_styles(template_style)

    # Process content for section blocks
    html_content = process_section_blocks(html_content)

    # Create complete HTML document
    html_template = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
{css_styles}
    </style>
</head>
<body>
    <div class="container">
        <header>
            {f'<img src="{header_image_path}" alt="Header Image">' if header_image_path else ''}
            <h1>{title}</h1>
            {f'<p>{subtitle}</p>' if subtitle else ''}
        </header>

        <div class="content">
            {html_content}
        </div>

        <footer>
            {f'<img src="{footer_image_path}" alt="Footer Image">' if footer_image_path else ''}
            <p>報告生成時間：{datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}</p>
        </footer>
    </div>
</body>
</html>"""

    return html_template


def process_section_blocks(html_content):
    """
    Process HTML content to add section blocks with appropriate classes
    """
    import re

    # Define section patterns and their corresponding classes
    section_patterns = {
        r'<h2[^>]*>.*?會議資訊.*?</h2>': 'meeting-info',
        r'<h2[^>]*>.*?會議概述.*?</h2>': 'meeting-info',
        r'<h2[^>]*>.*?技術背景.*?</h2>': 'tech-background',
        r'<h2[^>]*>.*?核心觀點.*?</h2>': 'core-insights',
        r'<h2[^>]*>.*?核心洞察.*?</h2>': 'core-insights',
        r'<h2[^>]*>.*?實踐經驗.*?</h2>': 'practical-experience',
        r'<h2[^>]*>.*?實際應用.*?</h2>': 'practical-experience',
    }

    # Split content by h2 tags
    sections = re.split(r'(<h2[^>]*>.*?</h2>)', html_content)

    processed_sections = []
    current_section_class = 'content-section'  # default class

    for i, section in enumerate(sections):
        if section.startswith('<h2'):
            # This is a header, determine the section class
            for pattern, class_name in section_patterns.items():
                if re.search(pattern, section, re.IGNORECASE):
                    current_section_class = class_name
                    break
            else:
                current_section_class = 'content-section'

            # Add section title class to h2
            section = section.replace('<h2', '<h2 class="section-title"')
            processed_sections.append(f'<div class="section-block {current_section_class}">')
            processed_sections.append(section)
        elif section.strip():
            # This is content
            processed_sections.append(section)
            if i == len(sections) - 1 or (i + 1 < len(sections) and sections[i + 1].startswith('<h2')):
                processed_sections.append('</div>')

    # If the last section wasn't closed, close it
    if processed_sections and not processed_sections[-1].endswith('</div>'):
        processed_sections.append('</div>')

    return ''.join(processed_sections)


# Preload template content for better performance
TEMPLATE_CACHE = {}

def get_cached_css_styles(template_style):
    """
    Get cached CSS styles for better performance
    """
    if template_style not in TEMPLATE_CACHE:
        TEMPLATE_CACHE[template_style] = get_css_styles(template_style)
    return TEMPLATE_CACHE[template_style]


def batch_convert_markdown_files(input_dir, output_dir, template_style="professional"):
    """
    Batch convert markdown files to HTML
    """
    import glob

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    markdown_files = glob.glob(os.path.join(input_dir, "*.md"))

    for md_file in markdown_files:
        with open(md_file, 'r', encoding='utf-8') as f:
            markdown_content = f.read()

        # Extract title from filename
        title = os.path.splitext(os.path.basename(md_file))[0]

        # Convert to HTML
        html_content = convert_markdown_to_html(
            markdown_content,
            template_style=template_style,
            title=title
        )

        # Save HTML file
        html_file = os.path.join(output_dir, f"{title}.html")
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"Converted: {md_file} -> {html_file}")


if __name__ == "__main__":
    # Example usage
    sample_markdown = """
# 技術報告範例

## 會議資訊
- 會議名稱：QCon Beijing 2025
- 時間：2025年3月
- 地點：北京

## 技術背景
這是技術背景的內容...

## 核心觀點
這是核心觀點的內容...

## 實踐經驗
這是實踐經驗的內容...
"""

    html_output = convert_markdown_to_html(
        sample_markdown,
        template_style="professional",
        title="測試報告",
        subtitle="基於 sample_630.html 設計風格"
    )

    print("HTML conversion completed successfully!")

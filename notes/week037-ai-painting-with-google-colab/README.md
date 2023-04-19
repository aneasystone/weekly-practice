# WEEK037 - 使用 Google Colab 体验 AI 绘画

[AIGC](https://wiki.mbalib.com/wiki/AIGC) 的全称为 AI Generated Content，是指利用人工智能技术来生成内容，被认为是继 PGC（Professionally Generated Content，专业生成内容）和 UGC（User Generated Content，用户生成内容）之后的一种新型内容创作方式。目前，这种创作方式一般可分为两大派别：一个是以 [OpenAI](https://openai.com/) 的 [ChatGPT](https://chat.openai.com/) 和 [GPT-4](https://openai.com/product/gpt-4)、Facebook 的 [LLaMA](https://github.com/facebookresearch/llama)、斯坦福的 [Alpaca](https://github.com/tatsu-lab/stanford_alpaca) 等 **大语言模型** 技术为代表的文本生成派，另一个是以 [Stability AI](https://stability.ai/) 的 [Stable Diffusion](https://github.com/CompVis/stable-diffusion)、[Midjourney](https://www.midjourney.com/home/)、OpenAI 的 [DALL·E 2](https://openai.com/product/dall-e-2) 等 **扩散模型** 技术为代表的图片生成派。

在文本生成方面，目前 AI 已经可以和用户聊天，回答各种问题，而且可以基于用户的要求进行文本创作，比如写文案、写邮件、写小说等；在图片生成方面，AI 的绘画水平也突飞猛进，目前 AI 已经可以根据用户的提示词创作出各种不同风格的绘画作品，而且可以对图片进行风格迁移、自动上色、缺损修复等，AI 生成的作品几乎可以媲美专业画师，生成作品的效率越来越高，而生成作品的成本却越来越低，这让 AI 绘画技术得以迅速普及，让普通用户也可以体验专业画师的感觉，我从小就很特别羡慕那些会画画的人，现在就可以借助 AI 技术让我实现一个画家的梦。

## AI 绘画的发展历史

2014 年 10 月，Ian J. Goodfellow 等人发表了一篇论文 [《Generative Adversarial Networks》](https://arxiv.org/abs/1406.2661)，在论文中提出了一种新的深度学习算法 GAN（生成式对抗网络），这个算法包含两个模型：**生成模型**（Generative Model，简称 G 模型）和 **判别模型**（Discriminative Model，简称 D 模型），在训练过程中，G 模型的目标是尽量生成以假乱真的图片去欺骗 D 模型，而 D 模型的目标是判断 G 模型生成的图片是不是真实的，这样，G 模型和 D 模型就构成了一个动态的博弈过程，仿佛老顽童周伯通的左右手互搏一样，当 D 模型无法判断输入的图片是 G 模型生成的还是真实的时候，G 模型和 D 模型的训练就达到了平衡，这时我们得到的 G 模型就可以生成以假乱真的图片了。

不过由于 GAN 算法包含了两个模型，稳定性较差，可能出现有趣的 **海奥维提卡现象（the helvetica scenario）**，如果 G 模型发现了一个能够骗过 D 模型的 bug，它就会开始偷懒，一直用这张图片来欺骗 D 模型，导致整个平衡的无效。在 2020 年，Jonathan Ho 等人发表论文 [《Denoising Diffusion Probabilistic Models》](https://arxiv.org/abs/2006.11239)，提出了一种新的 **扩散模型**（Diffusion Model），相比 GAN 来说，扩散模型的训练更稳定，而且能够生成更多样的样本，一时间扩散模型在 AI 圈里迅速起飞，2021 年 11 月 OpenAI 推出 DALL·E，2022 年 3 月，David Holz 推出 Midjourney，5 月 Google Brain 推出 Imagen，都是基于扩散模型实现的。

Stable Diffusion

## Google Colab 入门

https://colab.research.google.com/

## 在 Google Colab 里运行 Stable Diffusion

https://github.com/camenduru/stable-diffusion-webui-colab

## 参考

* [保姆级GPU白嫖攻略](https://cuijiahua.com/blog/2021/01/dl-basics-4.html)
* [ChatGPT 与 Midjourney 强强联手，让先秦阿房宫重现辉煌！](https://mp.weixin.qq.com/s/oE-qQJV7K_nVx6Zq88efhw)
* [零基础入门 Stable Diffusion - 无需显卡把 AI 绘画引擎搬进家用电脑](https://newzone.top/_posts/2022-09-05-stable_diffusion_ai_painting.html)

## 更多

### 文本生成派

* [ChatGPT](https://chat.openai.com/)
* [GPT-4](https://openai.com/product/gpt-4)
* [Claude AI](https://www.anthropic.com/claude-in-slack)
* [Google Bard](https://bard.google.com/)
* [Notion AI](https://www.notion.so/product/ai)

### 图片生成派

* [Midjourney](https://www.midjourney.com/home/)
* [Stability.AI](https://stability.ai/)
* [DALL.E.2](https://openai.com/product/dall-e-2)
* [Imagen](https://imagen.research.google/)
* [NovelAI](https://novelai.net/)

# WEEK053 - 开源大模型 Llama 实战

去年 2 月 24 号，Facebook 的母公司 [Meta AI 推出 Llama 语言模型](https://ai.meta.com/blog/large-language-model-llama-meta-ai/)，该模型完全使用公开可用的数据集进行训练，拥有 70 亿到 650 亿个参数，包括 `7B`、`13B`、`30B` 和 `65B` 四个版本，可以进行本地部署和微调训练，非常适合个人和中小型企业。OpenAI 对于 GPT-2 之后的模型就不再开源，这个时候 Meta 推出的 Llama 补上了这个缺口，掀起了开源大模型的发展浪潮。

到了 7 月，Meta AI 联合 Microsoft [又推出了 Llama 2 模型](https://ai.meta.com/blog/llama-2/)，将预训练语料库的大小增加了 40%，将模型的上下文长度增加了一倍，并采用了分组查询注意力，参数范围从 70 亿到 700 亿，包括 `7B`、`13B` 和 `70B` 三个版本。同时还发布了 Llama 2 的微调版本 Llama 2-Chat，专门针对聊天场景进行了优化。

## 模型下载

想要体验 Llama 模型，我们首先得把模型给下载下来，这里总结几种不同的下载方法。

### 官方版本下载

[根据官方仓库的说明](https://github.com/facebookresearch/llama)，我们需要填写一份表单进行申请：

* [Llama 申请](https://forms.gle/jk851eBVbX1m5TAv5)
* [Llama 2 申请](https://llama.meta.com/llama-downloads/)

当申请通过后，你会收到一份带有下载链接的邮件。然后下载 Llama 仓库的源码，执行其中的 `download.sh` 脚本：

```
$ git clone https://github.com/meta-llama/llama.git
$ cd llama
$ ./download.sh 
Enter the URL from email:
```

按提示输入邮件中的下载链接即可。

值得注意的是，这个下载脚本依赖于 `wget` 和 `md5sum` 命令，确保你的系统上已经安装了下面这两个工具：

```
$ brew install wget md5sha1sum
```

### 泄露版本下载

如果嫌从官方下载太麻烦，网上也有一些泄露的模型版本可以直接下载。

[这里](https://ipfs.io/ipfs/Qmb9y5GCkTG7ZzbBWMu2BXwMkzyCKcUjtEKPpgdZ7GEFKm/) 应该是最早泄漏的版本，可以使用 [IPFS 客户端](https://docs.ipfs.tech/install/ipfs-desktop/) 进行下载。

社区里也有人制作了种子，可以使用 BitTorrent 下载，磁链地址为 `magnet:?xt=urn:btih:ZXXDAUWYLRUXXBHUYEMS6Q5CE5WA3LVA&dn=LLaMA`。

### 使用 `pyllama` 下载

另一种下载 Llama 模型的方法是使用 [pyllama](https://github.com/juncongmoo/pyllama) 库。首先，通过 pip 安装它：

```
$ pip3 install transformers pyllama -U
```

然后通过下面的命令下载 Llama `7B` 模型（根据需要你也可以下载 `13B`、`30B` 和 `65B`，如果不指定 `--model_size` 则下载所有）：

```
$ python3 -m llama.download --model_size 7B
```

在 Mac M2 下可能会遇到下面这样的报错：

```
ImportError: dlopen(/Library/Python/3.9/site-packages/_itree.cpython-39-darwin.so, 0x0002): 
    tried: '/Library/Python/3.9/site-packages/_itree.cpython-39-darwin.so' 
    (mach-o file, but is an incompatible architecture (have 'x86_64', need 'arm64')), 
    '/System/Volumes/Preboot/Cryptexes/OS/Library/Python/3.9/site-packages/_itree.cpython-39-darwin.so' 
    (no such file), 
    '/Library/Python/3.9/site-packages/_itree.cpython-39-darwin.so' 
    (mach-o file, but is an incompatible architecture (have 'x86_64', need 'arm64'))
```

根据 [itree 的官方文档](https://github.com/juncongmoo/itree#build-from-source-with-cmake)，这个库我们需要自己手动构建：

```
$ brew install cmake
$ pip3 install https://github.com/juncongmoo/itree/archive/refs/tags/v0.0.18.tar.gz
```

安装完成后，再次下载，这次虽然没有报错，但是模型的下载目录 pyllama_data 却是空的，根据 [这里](https://github.com/juncongmoo/pyllama/issues/47) 的解决方案，我们使用源码重新安装 pyllama：

```
$ pip3 uninstall pyllama
$ git clone https://github.com/juncongmoo/pyllama
$ pip3 install -e pyllama
```

然后再次下载即可，7B 模型文件大约 13G，下载速度取决于你的网速，成功后输出如下：

```
$ python3 -m llama.download --model_size 7B
❤️  Resume download is supported. You can ctrl-c and rerun the program to resume the downloading

Downloading tokenizer...
✅ pyllama_data/tokenizer.model
✅ pyllama_data/tokenizer_checklist.chk
tokenizer.model: OK

Downloading 7B

downloading file to pyllama_data/7B/consolidated.00.pth ...please wait for a few minutes ...
✅ pyllama_data/7B/consolidated.00.pth
✅ pyllama_data/7B/params.json
✅ pyllama_data/7B/checklist.chk

Checking checksums for the 7B model
consolidated.00.pth: OK
params.json: OK
```

一共有 5 个文件：

```
$ tree pyllama_data
pyllama_data
|-- 7B
|   |-- checklist.chk
|   |-- consolidated.00.pth
|   `-- params.json
|-- tokenizer.model
`-- tokenizer_checklist.chk

2 directories, 5 files
```

## 模型推理

从下载文件 `consolidated.00.pth` 的后缀可以看出这是一个 [PyTorch](https://pytorch.org/) 中用于保存模型权重的文件，该文件包含了模型在训练过程中学到的权重参数，我们可以通过 PyTorch 提供的加载机制重新装载到相同或者相似结构的模型中，从而继续训练或者进行推理。

官方已经提供了这样的示例代码，可以对模型进行测试，我们先下载代码：

```
$ git clone https://github.com/meta-llama/llama.git
$ cd llama
$ git checkout llama_v1
```

注意切换到 `llama_v1` 分支，因为我们下的是 Llama 1 模型。然后安装所需依赖：

```
$ pip3 install -r requirements.txt
```

然后安装 Llama：

```
$ pip3 install -e .
```

最后运行下面的命令测试模型：

```
$ torchrun --nproc_per_node 1 example.py --ckpt_dir ../pyllama_data/7B --tokenizer_path ../pyllama_data/tokenizer.model
```

运行这个命令需要具备 NVIDIA 卡并且需要安装 CUDA，否则很可能会报下面这样的错：

```
Traceback (most recent call last):
  File "/Users/aneasystone/Codes/github/llama/example.py", line 119, in <module>
    fire.Fire(main)
  File "/Library/Python/3.9/site-packages/fire/core.py", line 141, in Fire
    component_trace = _Fire(component, args, parsed_flag_args, context, name)
  File "/Library/Python/3.9/site-packages/fire/core.py", line 475, in _Fire
    component, remaining_args = _CallAndUpdateTrace(
  File "/Library/Python/3.9/site-packages/fire/core.py", line 691, in _CallAndUpdateTrace
    component = fn(*varargs, **kwargs)
  File "/Users/aneasystone/Codes/github/llama/example.py", line 74, in main
    local_rank, world_size = setup_model_parallel()
  File "/Users/aneasystone/Codes/github/llama/example.py", line 23, in setup_model_parallel
    torch.distributed.init_process_group("nccl")
  File "/Library/Python/3.9/site-packages/torch/distributed/c10d_logger.py", line 86, in wrapper
    func_return = func(*args, **kwargs)
  File "/Library/Python/3.9/site-packages/torch/distributed/distributed_c10d.py", line 1184, in init_process_group
    default_pg, _ = _new_process_group_helper(
  File "/Library/Python/3.9/site-packages/torch/distributed/distributed_c10d.py", line 1302, in _new_process_group_helper
    raise RuntimeError("Distributed package doesn't have NCCL built in")
RuntimeError: Distributed package doesn't have NCCL built in
```

在深度学习的训练和推理过程中，我们常常会遇到单机多卡或多机多卡的情况，这就会涉及到各个卡或节点之间的通信，这种通信被称为 **集合通信（Collective Communication
）**，而 [NCCL](https://developer.nvidia.com/nccl) 就是这样的一个集合通信库，它是英伟达基于自家 NVIDIA GPU 定制开发的一套开源集合通信库，可以通过 PCIe 和 NVLink 等高速互联从而实现高带宽和低延迟。除了 NCCL，还有一些其他的库可以选择，比如 [MPI](https://www.mpi-forum.org/) 接口的开源实现 [Open MPI](https://www.open-mpi.org/) 、Facebook 的 [Gloo](https://github.com/facebookincubator/gloo) 等。

为了让代码能在我的 Mac 上跑起来，我参考了 [这里](https://github.com/meta-llama/llama/issues/50) 和 [这里](https://github.com/meta-llama/llama/issues/112) 的方法，将代码中和 CUDA 有关的内容都删掉，虽然可以运行，模型也显示加载成功了，但是却一直没有运行结果。最后，参考网友 [b0kch01 的实现](https://github.com/b0kch01/llama-cpu)，还需要对参数做一些修改，然后将代码改成一次只处理一个提示词，再将机器上所有程序全部关闭，终于把 Llama 模型运行起来了：

```
$ torchrun --nproc_per_node 1 example.py --ckpt_dir ../pyllama_data/7B --tokenizer_path ../pyllama_data/tokenizer.model
Locating checkpoints
Found MP=1 checkpoints
Creating checkpoint instance...
Grabbing params...
Loading model arguments...
Creating tokenizer...
Creating transformer...

-- Creating embedding
-- Creating transformer blocks (32)
-- Adding output layers 
-- Precomputing frequencies

Loading checkpoint to model...done in 57.88 seconds
Creating LLaMA generator...done in 0.01 seconds
Loaded in 89.92 seconds
Enter prompt: 
```

等了 90 秒，模型加载成功，接着我们手动输入示例中的第一个提示词：

```
Enter prompt: I believe the meaning of life is
Starting generation with prompt: I believe the meaning of life is
Forwarding 38 times
responded in 472.85 seconds
I believe the meaning of life is to fulfill your purpose in life, and once you’ve done that, you live to serve others and to love others.
My goal is

==================================

Enter next prompt:
```

又等了将近 8 分钟，模型才慢吞吞地输出 150 个左右的字符。

## 模型量化

可以看到，就算是最小的 7B 模型，在一般的个人电脑上跑起来也是相当费劲。目前有很多方法在研究如何减少大模型的资源占用，例如 [llama.cpp](https://github.com/ggerganov/llama.cpp)，号称可以在树莓派上进行推理，最低只需要 4G 内存。

### llama.cpp

首先我们下载 `llama.cpp` 的源码：

```
$ git clone https://github.com/ggerganov/llama.cpp
$ cd llama.cpp
```

官方提供了很多种不同的编译方法，包括 `make`、`CMake` 和 `Zig` 等，你可以根据你的喜好进行选择。另外，它还支持苹果的 [Metal 框架](https://developer.apple.com/metal/)、不同的消息传递接口 [MPI](https://en.wikipedia.org/wiki/Message_Passing_Interface) 实现，比如 [MPICH](https://www.mpich.org/) 和 [Open MPI](https://www.open-mpi.org/) 以及大量的 [BLAS](https://en.wikipedia.org/wiki/Basic_Linear_Algebra_Subprograms) 库，具体的编译选项可以 [参考官方文档](https://github.com/ggerganov/llama.cpp?tab=readme-ov-file#build)。我们这里直接使用 `make` 命令编译：

```
$ make
```

在 Mac 上编译无需额外参数，`llama.cpp` 已经对 [Arm Neon](https://www.arm.com/technologies/neon) 做了优化，会自动启动 BLAS，在 M 系列芯片上，还会自动使用 Metal 框架，显著提升 GPU 推理速度。

编译完成后会在当前目录生成一些可执行文件，比如：

* `main` - 用于模型推理的主程序
* `quantize` - 用于模型量化
* `server` - 以服务器模式运行

```
$ pip3 install -r requirements.txt
$ python3 convert.py ../pyllama_data/7B
```

```
$ ls -lh ../pyllama_data/7B 
total 52679296
-rw-r--r--@ 1 aneasystone  staff   100B Mar  5  2023 checklist.chk
-rw-r--r--@ 1 aneasystone  staff    13G Mar  5  2023 consolidated.00.pth
-rw-r--r--@ 1 aneasystone  staff    13G Mar 24 15:33 ggml-model-f16.gguf
-rw-r--r--@ 1 aneasystone  staff   101B Mar  5  2023 params.json
```

```
$ ./quantize ../pyllama_data/7B/ggml-model-f16.gguf ../pyllama_data/7B/ggml-model-Q4_K_M.gguf Q4_K_M
```

```
$ ls -lh ../pyllama_data/7B 
total 60674720
-rw-r--r--@ 1 aneasystone  staff   100B Mar  5  2023 checklist.chk
-rw-r--r--@ 1 aneasystone  staff    13G Mar  5  2023 consolidated.00.pth
-rw-r--r--@ 1 aneasystone  staff   3.8G Mar 24 15:38 ggml-model-Q4_K_M.gguf
-rw-r--r--@ 1 aneasystone  staff    13G Mar 24 15:33 ggml-model-f16.gguf
-rw-r--r--@ 1 aneasystone  staff   101B Mar  5  2023 params.json
```

```
$ ./main -m ../pyllama_data/7B/ggml-model-Q4_K_M.gguf -n 128 -p "I believe the meaning of life is"
Log start
main: build = 2518 (ddf65685)
main: built with Apple clang version 15.0.0 (clang-1500.0.40.1) for arm64-apple-darwin22.6.0
main: seed  = 1711266065
llama_model_loader: loaded meta data with 17 key-value pairs and 291 tensors from ../pyllama_data/7B/ggml-model-Q4_K_M.gguf (version GGUF V3 (latest))
llama_model_loader: Dumping metadata keys/values. Note: KV overrides do not apply in this output.
llama_model_loader: - kv   0:                       general.architecture str              = llama
llama_model_loader: - kv   1:                               general.name str              = pyllama_data
llama_model_loader: - kv   2:                           llama.vocab_size u32              = 32000
llama_model_loader: - kv   3:                       llama.context_length u32              = 2048
llama_model_loader: - kv   4:                     llama.embedding_length u32              = 4096
llama_model_loader: - kv   5:                          llama.block_count u32              = 32
llama_model_loader: - kv   6:                  llama.feed_forward_length u32              = 11008
llama_model_loader: - kv   7:                 llama.rope.dimension_count u32              = 128
llama_model_loader: - kv   8:                 llama.attention.head_count u32              = 32
llama_model_loader: - kv   9:              llama.attention.head_count_kv u32              = 32
llama_model_loader: - kv  10:     llama.attention.layer_norm_rms_epsilon f32              = 0.000001
llama_model_loader: - kv  11:                          general.file_type u32              = 15
llama_model_loader: - kv  12:                       tokenizer.ggml.model str              = llama
llama_model_loader: - kv  13:                      tokenizer.ggml.tokens arr[str,32000]   = ["<unk>", "<s>", "</s>", "<0x00>", "<...
llama_model_loader: - kv  14:                      tokenizer.ggml.scores arr[f32,32000]   = [0.000000, 0.000000, 0.000000, 0.0000...
llama_model_loader: - kv  15:                  tokenizer.ggml.token_type arr[i32,32000]   = [2, 3, 3, 6, 6, 6, 6, 6, 6, 6, 6, 6, ...
llama_model_loader: - kv  16:               general.quantization_version u32              = 2
llama_model_loader: - type  f32:   65 tensors
llama_model_loader: - type q4_K:  193 tensors
llama_model_loader: - type q6_K:   33 tensors
llm_load_vocab: special tokens definition check successful ( 259/32000 ).
llm_load_print_meta: format           = GGUF V3 (latest)
llm_load_print_meta: arch             = llama
llm_load_print_meta: vocab type       = SPM
llm_load_print_meta: n_vocab          = 32000
llm_load_print_meta: n_merges         = 0
llm_load_print_meta: n_ctx_train      = 2048
llm_load_print_meta: n_embd           = 4096
llm_load_print_meta: n_head           = 32
llm_load_print_meta: n_head_kv        = 32
llm_load_print_meta: n_layer          = 32
llm_load_print_meta: n_rot            = 128
llm_load_print_meta: n_embd_head_k    = 128
llm_load_print_meta: n_embd_head_v    = 128
llm_load_print_meta: n_gqa            = 1
llm_load_print_meta: n_embd_k_gqa     = 4096
llm_load_print_meta: n_embd_v_gqa     = 4096
llm_load_print_meta: f_norm_eps       = 0.0e+00
llm_load_print_meta: f_norm_rms_eps   = 1.0e-06
llm_load_print_meta: f_clamp_kqv      = 0.0e+00
llm_load_print_meta: f_max_alibi_bias = 0.0e+00
llm_load_print_meta: f_logit_scale    = 0.0e+00
llm_load_print_meta: n_ff             = 11008
llm_load_print_meta: n_expert         = 0
llm_load_print_meta: n_expert_used    = 0
llm_load_print_meta: causal attn      = 1
llm_load_print_meta: pooling type     = 0
llm_load_print_meta: rope type        = 0
llm_load_print_meta: rope scaling     = linear
llm_load_print_meta: freq_base_train  = 10000.0
llm_load_print_meta: freq_scale_train = 1
llm_load_print_meta: n_yarn_orig_ctx  = 2048
llm_load_print_meta: rope_finetuned   = unknown
llm_load_print_meta: ssm_d_conv       = 0
llm_load_print_meta: ssm_d_inner      = 0
llm_load_print_meta: ssm_d_state      = 0
llm_load_print_meta: ssm_dt_rank      = 0
llm_load_print_meta: model type       = 7B
llm_load_print_meta: model ftype      = Q4_K - Medium
llm_load_print_meta: model params     = 6.74 B
llm_load_print_meta: model size       = 3.80 GiB (4.84 BPW) 
llm_load_print_meta: general.name     = pyllama_data
llm_load_print_meta: BOS token        = 1 '<s>'
llm_load_print_meta: EOS token        = 2 '</s>'
llm_load_print_meta: UNK token        = 0 '<unk>'
llm_load_print_meta: LF token         = 13 '<0x0A>'
llm_load_tensors: ggml ctx size =    0.22 MiB
ggml_backend_metal_buffer_from_ptr: allocated buffer, size =  3820.94 MiB, ( 3821.00 / 10922.67)
llm_load_tensors: offloading 32 repeating layers to GPU
llm_load_tensors: offloading non-repeating layers to GPU
llm_load_tensors: offloaded 33/33 layers to GPU
llm_load_tensors:      Metal buffer size =  3820.93 MiB
llm_load_tensors:        CPU buffer size =    70.31 MiB
..................................................................................................
llama_new_context_with_model: n_ctx      = 512
llama_new_context_with_model: n_batch    = 512
llama_new_context_with_model: n_ubatch   = 512
llama_new_context_with_model: freq_base  = 10000.0
llama_new_context_with_model: freq_scale = 1
ggml_metal_init: allocating
ggml_metal_init: found device: Apple M2
ggml_metal_init: picking default device: Apple M2
ggml_metal_init: default.metallib not found, loading from source
ggml_metal_init: GGML_METAL_PATH_RESOURCES = nil
ggml_metal_init: loading '/Users/zhangchangzhi/Codes/github/llama.cpp/ggml-metal.metal'
ggml_metal_init: GPU name:   Apple M2
ggml_metal_init: GPU family: MTLGPUFamilyApple8  (1008)
ggml_metal_init: GPU family: MTLGPUFamilyCommon3 (3003)
ggml_metal_init: GPU family: MTLGPUFamilyMetal3  (5001)
ggml_metal_init: simdgroup reduction support   = true
ggml_metal_init: simdgroup matrix mul. support = true
ggml_metal_init: hasUnifiedMemory              = true
ggml_metal_init: recommendedMaxWorkingSetSize  = 11453.25 MB
ggml_backend_metal_buffer_type_alloc_buffer: allocated buffer, size =   256.00 MiB, ( 4078.00 / 10922.67)
llama_kv_cache_init:      Metal KV buffer size =   256.00 MiB
llama_new_context_with_model: KV self size  =  256.00 MiB, K (f16):  128.00 MiB, V (f16):  128.00 MiB
llama_new_context_with_model:        CPU  output buffer size =    62.50 MiB
ggml_backend_metal_buffer_type_alloc_buffer: allocated buffer, size =    70.50 MiB, ( 4148.50 / 10922.67)
llama_new_context_with_model:      Metal compute buffer size =    70.50 MiB
llama_new_context_with_model:        CPU compute buffer size =     9.00 MiB
llama_new_context_with_model: graph nodes  = 1060
llama_new_context_with_model: graph splits = 2

system_info: n_threads = 4 / 8 | AVX = 0 | AVX_VNNI = 0 | AVX2 = 0 | AVX512 = 0 | AVX512_VBMI = 0 | AVX512_VNNI = 0 | FMA = 0 | NEON = 1 | ARM_FMA = 1 | F16C = 0 | FP16_VA = 1 | WASM_SIMD = 0 | BLAS = 1 | SSE3 = 0 | SSSE3 = 0 | VSX = 0 | MATMUL_INT8 = 0 | 
sampling: 
        repeat_last_n = 64, repeat_penalty = 1.000, frequency_penalty = 0.000, presence_penalty = 0.000
        top_k = 40, tfs_z = 1.000, top_p = 0.950, min_p = 0.050, typical_p = 1.000, temp = 0.800
        mirostat = 0, mirostat_lr = 0.100, mirostat_ent = 5.000
sampling order: 
CFG -> Penalties -> top_k -> tfs_z -> typical_p -> top_p -> min_p -> temperature 
generate: n_ctx = 512, n_batch = 2048, n_predict = 128, n_keep = 1


I believe the meaning of life is to serve others. As a doctor, I want to help those in need and make a difference in their lives.
I believe the meaning of life is to serve others. As a doctor, I want to help those in need and make a difference in their lives. 
I am honored to be able to do just that in my community.
I love meeting new people and developing relationships with them. My goal is to provide high-quality care in a relaxed and comfortable environment. 
I take the time to listen to each patient and get to know them on a personal level.
I believe that a healthy life starts with prevent
llama_print_timings:        load time =    1040.38 ms
llama_print_timings:      sample time =       2.49 ms /   128 runs   (    0.02 ms per token, 51384.99 tokens per second)
llama_print_timings: prompt eval time =     231.36 ms /     8 tokens (   28.92 ms per token,    34.58 tokens per second)
llama_print_timings:        eval time =    6948.32 ms /   127 runs   (   54.71 ms per token,    18.28 tokens per second)
llama_print_timings:       total time =    7196.03 ms /   135 tokens
ggml_metal_free: deallocating
Log end
```

```
$ ./server -m ../pyllama_data/7B/ggml-model-Q4_K_M.gguf -c 1024
...
{"tid":"0x1fd44a080","timestamp":1711270965,"level":"INFO","function":"init","line":702,"msg":"initializing slots","n_slots":1}
{"tid":"0x1fd44a080","timestamp":1711270965,"level":"INFO","function":"init","line":714,"msg":"new slot","id_slot":0,"n_ctx_slot":1024}
{"tid":"0x1fd44a080","timestamp":1711270965,"level":"INFO","function":"main","line":2881,"msg":"model loaded"}
{"tid":"0x1fd44a080","timestamp":1711270965,"level":"INFO","function":"main","line":2906,"msg":"chat template","chat_example":"<|im_start|>system\nYou are a helpful assistant<|im_end|>\n<|im_start|>user\nHello<|im_end|>\n<|im_start|>assistant\nHi there<|im_end|>\n<|im_start|>user\nHow are you?<|im_end|>\n<|im_start|>assistant\n","built_in":true}
{"tid":"0x1fd44a080","timestamp":1711270965,"level":"INFO","function":"main","line":3524,"msg":"HTTP server listening","port":"8080","n_threads_http":"7","hostname":"127.0.0.1"}
```

### pyllama

https://github.com/juncongmoo/pyllama

```
$ pip3 install gptq
```

### Ollama

https://github.com/ollama/ollama

https://ollama.com/blog/run-code-llama-locally

https://ollama.com/library

https://python.langchain.com/docs/guides/local_llms

### PrivateGPT

https://docs.privategpt.dev/overview/welcome/introduction

### GPT4All

https://github.com/nomic-ai/gpt4all

## 模型微调

Meta 最初发布的 Llama 模型并没有进行指令微调，于是斯坦福马上公布了 Alpaca 模型，该模型是由 Llama 7B 利用 52k 的指令微调出来的。

https://github.com/tatsu-lab/stanford_alpaca

https://github.com/tloen/alpaca-lora

https://github.com/ymcui/Chinese-LLaMA-Alpaca

https://github.com/LC1332/Luotuo-Chinese-LLM

https://llama.meta.com/

https://github.com/facebookresearch/llama-recipes/

## 参考

* [NCCL、OpenMPI、Gloo对比](https://blog.csdn.net/taoqick/article/details/126449935)
* [如何评价 LLaMA 模型泄露？](https://www.zhihu.com/question/587479829)
* [Run LLMs locally](https://python.langchain.com/docs/guides/local_llms)
* [本地部署开源大模型的完整教程：LangChain + Streamlit+ Llama](https://zhuanlan.zhihu.com/p/639565332)
* [用 Ollama 轻松玩转本地大模型](https://sspai.com/post/85193)
* [Mac 上 LLAMA2 大语言模型安装到使用](https://my.oschina.net/qyhstech/blog/11046186)
* [用筆電就能跑 LLaMA 2! llama.cpp 教學](https://medium.com/@cch.chichieh/%E7%94%A8%E6%89%8B%E6%A9%9F%E5%B0%B1%E8%83%BD%E8%B7%91-llama-2-llama-cpp-%E6%95%99%E5%AD%B8-2451807f8ba5)
* [Beyond LLaMA: The Power of Open LLMs](https://cameronrwolfe.substack.com/p/beyond-llama-the-power-of-open-llms)
* [Efficiently Run Your Fine-Tuned LLM Locally Using Llama.cpp](https://medium.com/vendi-ai/efficiently-run-your-fine-tuned-llm-locally-using-llama-cpp-66e2a7c51300)
* [How is LLaMa.cpp possible?](https://finbarr.ca/how-is-llama-cpp-possible/)

## 更多

### 其他大模型

* [本地运行“李开复”的零一万物 34B 大模型](https://soulteary.com/2023/11/26/locally-run-the-yi-34b-large-model-of-kai-fu-lee.html)
* [手把手教大家从搭建环境开始实现本地部署ChatGLM2 6B 大模型](https://zhuanlan.zhihu.com/p/668773349)
* [如何真正“不花一分钱”部署一个属于你的大模型](https://www.cnblogs.com/rude3knife/p/llm-free-deploy.html)

### 其他推理框架

* [本地化大模型部署：LocalGPT应用指南](https://www.51cto.com/article/778996.html)
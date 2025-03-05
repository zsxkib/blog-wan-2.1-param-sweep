# WAN parameter sweep tool

[![Replicate](https://replicate.com/wavespeedai/wan-2.1-t2v-720p/badge)](https://replicate.com/wavespeedai/wan-2.1-t2v-720p)

This is the code we used in our [blog post about WAN2.1 parameters](https://replicate.com/blog/wan-21-parameter-sweep). Curious how different settings affect your text-to-video results? Run your own parameter sweep to see what happens.

## What these parameters actually do

Two settings make a huge difference in your video results:

- `sample_guide_scale`: The "creativity vs obedience" knob (0 to 10)
- `sample_shift`: Controls the "flow of time" in your video (1 to 9)

We use sensible defaults for whichever parameter you're not testing:
- When exploring `sample_shift`, we set `sample_guide_scale` to 7 (good obedience without the weird AI shine)
- When exploring `sample_guide_scale`, we set `sample_shift` to 5 (balanced motion)

## How to run it

First, you need a Replicate API token:

```bash
export REPLICATE_API_TOKEN=your_token_here
```

### Quick start

```bash
# See what happens with different guide scale values
python wan.py

# Or explore different shift values instead
python wan.py --type shift
```

### Make it your own

```bash
# Try a different prompt
python wan.py --prompt "A raccoon playing drums in a rock concert"

# Use a specific seed for consistent comparisons
python wan.py --seed 123

# Run more videos in parallel (default: 5)
python wan.py --workers 3

# Try a different model
python wan.py --model "alternative-model/version"

# Mix and match options
python wan.py --type shift --prompt "Astronaut riding a horse" --seed 42 --workers 4
```

## Where to find your videos

Your parameter sweep videos go to:
- `guide_comparison/` folder when varying guide scale
- `shift_comparison/` folder when varying shift

Each file is named by its parameter value (like `guide7.mp4` or `shift3.mp4`).

## What you need to run it

- Python 3.6+
- `replicate` package
- `requests` package

## Tips from our experiments

- Use a fixed seed so the only difference is the parameter you're changing
- For `guide_scale`, values between 3-7 give the most natural results
- Higher worker counts make things faster but might hit API rate limits
- The default prompt is "A smiling woman walking in London at night" (same as in our blog)
- Videos are 81 frames at 16fps in 16:9 aspect ratio

Found something cool in your experiments? I'd love to see it! Share your discoveries with me on Twitter [@zsakib_](https://twitter.com/zsakib_).

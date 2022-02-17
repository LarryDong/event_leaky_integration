# event_leaky_integration
Event leaky integration to reconstruct the intensity frame.

This method using `leaky-integration` model to reconstruct intensity frame from an event file.

Using equation:  
log(I(x), t) = log(I(x), 0) + C*p

## Usage
```bash
python leaky_integrate.py  --parameter=xxx
```

**Parameters**
@`width`, @`height`: image width and height
@`event_file`: event steam
@`duration`: required if no `image_ts` is provided. Default: 50ms
@`ts_file`: a reference image ts file. Optional, it not provided, using `duration`


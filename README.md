# event_leaky_integration

Event leaky integration to reconstruct the intensity frame.
<div align=center>
<img src="https://raw.githubusercontent.com/LarryDong/event_leaky_integration/main/image/1876.325.bmp" width="346" height="260" alt="leaky-integration"/><br/>
</div>


This method using `leaky-integration` model to reconstruct intensity frame from an event file.

`leaky-integration` model:  `log(I(x), t) = log(I(x), 0) + C*p`


For more details, check the file from TU Berlin's course: [https://drive.google.com/file/d/1MtbzVMKebJq2I0FaG6CtmH0gEomAJ19h/view](https://drive.google.com/file/d/1MtbzVMKebJq2I0FaG6CtmH0gEomAJ19h/view)


## Usage
```bash
python leaky_integrate.py  --parameter=xxx
```

**Parameters**  
@`width`, @`height`: image width and height  
@`event_file`: event steam  
@`duration`: required if no `image_ts` is provided. Default: 50ms  
@`ts_file`: a reference image ts file. Optional, it not provided, using `duration`  


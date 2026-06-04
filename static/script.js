document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('upload-form');
    const imageInput = document.getElementById('image-input');
    const originalImage = document.getElementById('original-image');
    const maskImage = document.getElementById('mask-image');
    const overlayImage = document.getElementById('overlay-image');
    const loading = document.getElementById('loading');

    // Lấy phần tử tia quét laser từ UI mới
    const scanLine = document.querySelector('.scan-line');

    // Display selected image
    imageInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                originalImage.src = e.target.result;
                originalImage.style.display = 'block';

                // Ẩn các ảnh kết quả cũ và tia quét khi đổi ảnh mới
                maskImage.style.display = 'none';
                overlayImage.style.display = 'none';
                if (scanLine) scanLine.classList.add('hidden');
            };
            reader.readAsDataURL(file);
        }
    });

    // Handle form submission
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const file = imageInput.files[0];
        if (!file) {
            alert('Please select an image first');
            return;
        }

        // Bật trạng thái Loading hologram và Tia quét Laser
        loading.classList.remove('hidden');
        if (scanLine) scanLine.classList.remove('hidden');

        // Create form data
        const formData = new FormData();
        formData.append('file', file);

        try {
            // Send request to backend
            const response = await fetch('/predict', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const result = await response.json();

            // Display all images
            originalImage.src = `data:image/png;base64,${result.original}`;
            maskImage.src = `data:image/png;base64,${result.mask}`;
            overlayImage.src = `data:image/png;base64,${result.overlay}`;

            originalImage.style.display = 'block';
            maskImage.style.display = 'block';
            overlayImage.style.display = 'block';
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while processing the image');
        } finally {
            // Tắt hiệu ứng loading và tia quét sau khi xử lý xong
            loading.classList.add('hidden');
            if (scanLine) scanLine.classList.add('hidden');
        }
    });

    // ==========================================
    // HIỆU ỨNG TƯƠNG TÁC 3D GÓC NGHIÊNG (TILT EFFECT)
    // ==========================================
    const cards = document.querySelectorAll('.glass-card');

    cards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();

            // Lấy tọa độ chuột tương đối bên trong thẻ card
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            // Tính toán tâm của thẻ
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;

            // Tính toán góc nghiêng dựa trên khoảng cách từ chuột đến tâm (Giới hạn tối đa ~10 độ)
            const rotateX = ((centerY - y) / centerY) * 10;
            const rotateY = ((x - centerX) / centerX) * 10;

            // Áp dụng trực tiếp hiệu ứng chuyển động 3D cho thẻ
            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-8px) scale(1.02)`;
        });

        // Trả thẻ về trạng thái cân bằng ban đầu khi di chuột ra ngoài
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateY(0) scale(1)';
        });
    });
});